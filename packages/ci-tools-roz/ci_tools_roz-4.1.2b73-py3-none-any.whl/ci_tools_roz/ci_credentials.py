#!/usr/bin/env python3
import argparse
import json
import os
import sys
import uuid

import boto3

CI_ACCOUNT = '763500167284'  # sharedservices-prod


def ci_credentials(service, region):
    """ Get the credentials for a given service
    :param service: The name of the service
    :param region: The region for the service
    :returns: Returns the credentials as a json string containing user and password items"""

    if service is None:
        raise ValueError('Service must be specified')

    # We need to assume to the ci_secrets_access role in the CI_ACCOUNT account
    # To access the secrets stored there
    session = boto3.Session(region_name=region)
    my_account = boto3.client('sts').get_caller_identity().get('Account')
    if my_account == CI_ACCOUNT:
        access_role_arn = f'arn:aws:iam::{CI_ACCOUNT}:role/ci-prod-secrets-access'
    else:
        access_role_arn = f'arn:aws:iam::{CI_ACCOUNT}:role/ci-secrets-access'

    assumed_role = session.client('sts').assume_role(
        RoleArn=access_role_arn,
        RoleSessionName='secret-access' + uuid.uuid1().hex)

    assumed_session = boto3.Session(region_name=region,
                                    aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
                                    aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
                                    aws_session_token=assumed_role['Credentials']['SessionToken'])

    client = assumed_session.client('secretsmanager')
    secret_id = '/%s/ci/publish/credentials' % service.lower()
    cred = client.get_secret_value(SecretId=secret_id)['SecretString']
    return cred


def populate_credential(credentials, input_stream, output_stream):
    if not input_stream:
        output_stream.write(json.dumps(credentials, indent=2, default=str))
    else:
        content = input_stream.read()
        for k, v in credentials.items():
            content = content.replace('%%%%::%s::%%%%' % k, v)
        output_stream.write(content)


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(description='Fetch the lastest CI password '
                                                 'for a given service, and populate it '
                                                 'into the template file.')
    parser.add_argument('service', type=str,
                        help="The service to retrieve the CI credentials from "
                             "Currently only 'nexus' supported",
                        default=None)

    parser.add_argument('-r', '--region', type=str,
                        help="Specify the region to find the credentials in",
                        default='ap-southeast-2')
    parser.add_argument('-i', '--input-file', type=str,
                        help="Optional: Specify the path of input template file. If not "
                             "provided, then this script won't do any templating, but simply"
                             "print the credentials to the output. The template is like %%::key::%%. "
                             "For example, %%::user::%% will be replaced by the actual user id in the credential "
                             "info. If does not exist in credential info, then the %%::user::%% will be kept "
                             "intact. The key is case sensitive. Thus %%::User::%% will not be replaced by the "
                             "'user' value in the credential info.",
                        default=None)
    parser.add_argument('-o', '--output-file', type=str,
                        help="Optional: Specify the out path of populated file. If not provided, "
                             "stdout will be used.",
                        default=None)

    args = parser.parse_args()
    input_stream = None if not args.input_file else open(os.path.expanduser(args.input_file), 'r')
    output_stream = sys.stdout if not args.output_file else open(os.path.expanduser(args.output_file), 'w')
    credential_obj = json.loads(ci_credentials(args.service, args.region))
    populate_credential(credential_obj, input_stream, output_stream)


if __name__ == '__main__':  # pragma: no cover
    main()
