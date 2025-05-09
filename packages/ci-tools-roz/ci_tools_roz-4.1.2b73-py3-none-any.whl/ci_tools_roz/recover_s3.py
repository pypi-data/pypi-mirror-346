#!/usr/bin/env python3
import calendar
import json
import logging
import os
import signal
import sys

import argparse
import boto3
import boto3.ec2

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def get_all_key_history_around_timestamp(versions_iter, recovery_timestamp):
    all_keys = {}
    count = 0
    for version in versions_iter:
        count += 1
        if count % 1000 == 0:
            logger.info("Collected %d", count)
        epoc = calendar.timegm(version.last_modified.timetuple())
        if version.object_key not in all_keys:  # meet for the first time, add it
            if epoc > recovery_timestamp:  # last state is after the recovery time
                all_keys[version.object_key] = [epoc, None, epoc, version]
            else:
                all_keys[version.object_key] = [epoc, version, epoc, version]
        else:
            if epoc > all_keys[version.object_key][2]:  # update latest version info
                all_keys[version.object_key][2] = epoc
                all_keys[version.object_key][3] = version
            if epoc > recovery_timestamp:
                continue
            if epoc > all_keys[version.object_key][0] or epoc > all_keys[version.object_key][1] is None:
                all_keys[version.object_key][0] = epoc
                all_keys[version.object_key][1] = version
    return all_keys


def analyze_todos(all_keys):
    """
    returns a list of versions to delete and a list of versions to recover.
    The version has the object key within it.
    """
    # when item.size is None: means it is deleted at that particular timestamp.
    delete_items = [v for v in all_keys.values() if (v[1] is None or v[1].size is None) and v[3].size is not None]
    recover_items = [v for v in all_keys.values() if (v[1] is not None and v[1].size is not None) and
                     (v[3].size is None or v[1].version_id != v[3].version_id)]
    return delete_items, recover_items


# pylint: disable=too-many-arguments,too-many-locals,too-many-branches
def recover_bucket_backup(bucket, s3_resource, client,
                          recovery_timestamp=None, dry_run=True, output=None):
    logger.info("Recovering with s3://%s to the timestamp %s", bucket,
                recovery_timestamp)

    backup_bucket_obj = s3_resource.Bucket(bucket)
    logger.info("Collecting with versions of keys...")
    # all_keys = {
    # s3_key:(
    #     0: timestamp the value(version) for [1]
    #     1: Which value(version) can stand for the state at the timestamp
    #     2: timestamp the latest version
    #     2: The latest value (version)
    # )
    # }
    all_keys = get_all_key_history_around_timestamp(backup_bucket_obj.object_versions.all(),
                                                    recovery_timestamp)
    delete_items, recover_items = analyze_todos(all_keys)
    if delete_items:
        logger.info("To delete %d items", len(delete_items))
        count = 0
        keyz = []
        for idx, item in enumerate(delete_items):
            keyz.append(item[3].object_key)
            if output:
                output.write("Delete key '%s' at version of time: '%s'\n" % (item[3].object_key, item[3].last_modified))
            count += 1
            if count % 1000 == 0 or idx == len(delete_items) - 1:
                if not dry_run:
                    r = client.delete_objects(
                        Bucket=bucket,
                        Delete={
                            'Objects': [
                                {
                                    'Key': k,
                                }
                                for k in keyz],
                        },
                    )
                    if 'Errors' in r:
                        logger.info("Try to delete %d, error: %s", count, json.dumps(r['Errors']))
                keyz = []
    else:
        logger.info("No key to delete")

    if recover_items:
        logger.info("To recover %d items", len(recover_items))
        count = 0
        for item in recover_items:
            count += 1
            if count % 100 == 0:
                logger.info("Recovered %d", count)
            if output:
                output.write("Recover key '%s' at version of time: '%s'\n" %
                             (item[1].object_key, item[1].last_modified))
            if not dry_run:
                s3_resource.meta.client.copy(
                    {
                        'Bucket': bucket,
                        'Key': item[1].object_key,
                        'VersionId': item[1].version_id
                    },
                    bucket, item[1].object_key)
    else:
        logger.info("No key to recover")


def signal_handler(s, f):  # pylint: disable=unused-argument
    logger.error('The process has been terminated unexpectedly. This is not ideal as part of the s3 keys'
                 'has been recovered to the state of desired timestamp, but the rest are not. You are strongly '
                 'suggested to re-run the command to keep processing.')
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def main():
    parser = argparse.ArgumentParser(
        description="Recovering a versioned S3 bucket to a particular timestamp. "
                    "NOTICE: This script works on a versioned s3 bucket and picks the objects "
                    "version at the exact timestamp and mark the versions as "
                    "'latest'. No object version history will be deleted. This script actually "
                    "'top up' more versions upon existing objects' version history.",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-b', '--buckets', default=[], action='append', required=True,
                        help='The list of buckets to be recovered. Can be multiple.')

    parser.add_argument('-t', '--recovery_timestamp', required=True, type=int,
                        help='OPTIONAL: Recover to the epoch seconds.'
                             'Used only when action is set to recover. If not specified, then means NOW. '
                             'Example: 1529902189. Use https://www.epochconverter.com to calculate'
                             'the epoch seconds value at your convenience. '
                             '')
    parser.add_argument('-p', '--profile', required=False, default=None,
                        help='OPTIONAL: The aws profile to operate the buckets.')

    parser.add_argument('-d', '--dry-run', required=False, default=False, action='store_true',
                        help='OPTIONAL: Only generate plots rather than execution.')

    parser.add_argument('-o', '--output-file', required=False, default=None,
                        help='OPTIONAL: Generate a execution report. If not provided, the report will be '
                             'printed on the stdout.')

    args = parser.parse_args()

    session = boto3.session.Session(profile_name=args.profile)
    client = session.client('s3')
    s3_resource = session.resource('s3')

    if args.output_file:
        output = open(os.path.expanduser(args.output_file), 'w')
    else:
        output = sys.stdout
    for bucket in args.buckets:
        if bucket.startswith("s3://"):
            bucket = bucket[5:]
        if bucket.endswith('/'):
            bucket = bucket[:-1]
        recover_bucket_backup(bucket, s3_resource, client, args.recovery_timestamp, args.dry_run, output)
    if args.output_file:
        output.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
