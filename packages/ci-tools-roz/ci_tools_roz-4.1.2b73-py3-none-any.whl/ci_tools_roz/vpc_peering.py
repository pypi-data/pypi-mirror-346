#!/usr/bin/env python3

import json
import sys
from time import sleep
from functools import reduce
import cli.log
import boto3
import yaml

import botocore  # For exceptions

RETRY_COUNT = 20
RETRY_SLEEP = 10  # Seconds
DEFAULT_REGION = 'ap-southeast-2'


def match_tag_prefix(logger, tag_list, prefix):
    """
    Check if tag_list matches the prefix.
    """
    if tag_list:
        for tag in tag_list:
            if tag['Key'] == "Name" and tag['Value'].startswith(prefix):
                logger.debug("match_tag_prefix: %s %s %s", prefix, tag['Value'], tag_list)
                return True

    return False


def filter_by_id_or_prefix(log, resources, some_id, vpc_name=None):
    """
    Filter an resource matching "some_id".
    It should be an resource id exact match, or a Tag:Name prefix match.
    """

    vpc_prefix = f'{vpc_name}-{some_id}'

    def filter_func(r):
        return r.id == some_id or \
               match_tag_prefix(log, r.tags, prefix=some_id) or \
               (vpc_name is not None and match_tag_prefix(log, r.tags, prefix=vpc_prefix))

    return [r for r in resources if filter_func(r)]


def beautify_routes_dest(route):
    return ":".join(filter(lambda x: x is not None,
                           (
                               route.vpc_peering_connection_id,
                               route.egress_only_internet_gateway_id,
                               route.gateway_id,
                               route.instance_id,
                               route.nat_gateway_id,
                               route.network_interface_id,
                           )))


def read_config(logger, filepath=None):
    logger.info("Reading config %s", filepath)
    try:
        with open(filepath) as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
    except (yaml.YAMLError, FileNotFoundError) as exc:
        logger.error("Failed to load config file: %s", exc)
        sys.exit(1)

    logger.info("Validating config")

    # Simple validation, doesn't cover all requirements (yet)
    required_fields = ['accepter', 'requester', 'routes']
    for f in required_fields:
        if f not in config:
            logger.error("%s section missing from config", f)
            sys.exit(1)
    for f in ['accepter', 'requester']:
        if isinstance(config[f]['acc'], int):
            logger.error("acc is an 'int'. Must be a string: %s", config[f])
            sys.exit(1)

    return config


def get_peers(vpc):
    result = []
    if vpc.accepted_vpc_peering_connections is not None:
        result.extend(vpc.accepted_vpc_peering_connections.all())
    if vpc.requested_vpc_peering_connections is not None:
        result.extend(vpc.requested_vpc_peering_connections.all())

    return result


def find_common_peer(config):
    # Find undeleted peers.
    # Deleted peers may remain for some time, so we ignore them

    config['requester']['existing_peer'] = [p for p in config['requester']['all_existing_peers']
                                            if p.accepter_vpc.id == config['accepter']['vpc_resource'].id
                                            and p.status['Code'] != 'deleted']

    config['accepter']['existing_peer'] = [p for p in config['accepter']['all_existing_peers']
                                           if p.requester_vpc.id == config['requester']['vpc_resource'].id
                                           and p.status['Code'] != 'deleted']

    return list(set(config['requester']['existing_peer'] + config['accepter']['existing_peer']))


def get_ec2(logger, boto_session, role=None, region=DEFAULT_REGION):
    if role:
        try:
            logger.info(f"Assuming to role: {role}")
            assumed_role = boto_session.client('sts').assume_role(RoleArn=role, RoleSessionName="peering")
            ec2_resource = boto3.resource('ec2',
                                          aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
                                          aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
                                          aws_session_token=assumed_role['Credentials']['SessionToken'],
                                          region_name=region)

            ec2_client = boto3.client('ec2',
                                      aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
                                      aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
                                      aws_session_token=assumed_role['Credentials']['SessionToken'],
                                      region_name=region)
        except botocore.exceptions.ClientError as exc:
            logger.error("Failed to assume role: %s", exc)
            sys.exit(1)
    else:
        logger.info("No role supplied, connecting directly")
        ec2_resource = boto_session.resource('ec2', region_name=region)
        ec2_client = boto_session.client('ec2', region_name=region)

    return ec2_resource, ec2_client


def analyse_account(logger, account_cfg, boto_session, region):
    role = account_cfg.get('credential').get('role') if account_cfg.get('credential') else None
    region = account_cfg.get('region', region)
    ec2_resource, ec2_client = get_ec2(logger, boto_session, role, region)

    try:
        all_vpcs = ec2_resource.vpcs.all()
    except botocore.exceptions.ClientError as exc:
        logger.error("Failed to list VPCs: %s", exc)
        sys.exit(1)

    found_vpcs = filter_by_id_or_prefix(logger, all_vpcs, account_cfg.get('vpc'), None)

    if not found_vpcs or len(found_vpcs) > 1:
        count = 0 if not found_vpcs else len(found_vpcs)
        logger.error("Expecting 1 VPC with Name / ID of '%s', found %d matches instead", account_cfg.get('vpc'), count)
        sys.exit(1)

    account_cfg['ec2_client'] = ec2_client
    account_cfg['vpc_resource'] = found_vpcs[0]

    if account_cfg['vpc_resource'].tags:
        for tag in account_cfg['vpc_resource'].tags:
            if tag['Key'] == 'Name':
                account_cfg['vpc_name'] = tag['Value']
                break

    if 'vpc_name' not in account_cfg:
        logger.error("The vpc '%s' does not have Name tag, which is required!", found_vpcs[0].id)
        sys.exit(1)

    account_cfg['all_existing_peers'] = get_peers(found_vpcs[0])


def action_apply(logger, config, common_peer, force):
    if common_peer:
        if not force:
            logger.error("There are existing peering between VPCs. Requester VPC:%s, accepter VPC:%s, "
                         "Peer :%s. Note the peer might be a faulty peer. You can proceed with --force option",
                         config['requester']['vpc_resource'].id,
                         config['accepter']['vpc_resource'].id,
                         common_peer[0])
            sys.exit(1)
        cleanup_peering(logger, config)
    setup_peering(logger, config)


def action_delete(logger, config, common_peer):
    if not common_peer:
        logger.info("No peer exists.")
    else:
        cleanup_peering(logger, config)


def action_plan(logger, config, common_peer):
    if common_peer:
        logger.warning("Peering already exists as %s. It will be deleted together with all the "
                       "routes associated with it.", common_peer[0].id)

    logger.info("A new peer will set up from requester(%s, %s) to accepter(%s, %s)",
                config['requester']['acc'], config['requester']['region'],
                config['accepter']['acc'], config['accepter']['region'])
    logger.info("Existing route tables will be updated as:")
    logger.info("At requester side, route table->accepter subnets: %s",
                json.dumps(config['desired']['requester'], indent=2, default=str))
    logger.info("At accepter side, route table->requester subnets: %s",
                json.dumps(config['desired']['accepter'], indent=2, default=str))


@cli.log.LoggingApp(stream=sys.stderr, description='''
The app to help setting up the peering between two VPCs.
Ideally, you should prepare your default aws config (or the --profile) as sysadmin account, which
will be used as requester, and allow sysadmin account to be able to assume to the accepter
account role. The role should be configured in the config yaml file.
''')
def vpc_peering(app):
    config = read_config(app.log, app.params.config)
    app.log.debug("Config: %s", json.dumps(config, indent=2, default=str))

    verify_vpcs(app.log, config, app.params.profile, app.params.region)
    app.log.info("Collected VPC details: %s", json.dumps(config, indent=2, default=str))

    analyse_route_config(app.log, config)
    app.log.info("Analysed Subnet config: %s", json.dumps(config, indent=2, default=str))

    common_peer = find_common_peer(config)
    app.log.debug("common_peer found: %s", common_peer)

    if app.params.action == 'apply':
        action_apply(app.log, config, common_peer, app.params.force)
    elif app.params.action == 'delete':
        action_delete(app.log, config, common_peer)
    elif app.params.action == 'plan':
        action_plan(app.log, config, common_peer)
    else:
        app.log.error(f'Unsupported action: {app.params.action}')


def create_peering_connection(logger, config):
    logger.info("Peering from requester(%s) to accepter(%s)", config['requester']['acc'], config['accepter']['acc'])
    local_vpc_id = config['requester']['vpc_resource'].id
    peer_vpc_id = config['accepter']['vpc_resource'].id
    peer_owner_id = config['accepter']['acc']
    peer_region = config['accepter']['region']

    logger.info("Requesting from requester(%s) side.", config['requester']['acc'])
    try:
        peering_id = config['requester']['ec2_client']. \
            create_vpc_peering_connection(
                VpcId=local_vpc_id,
                PeerVpcId=peer_vpc_id,
                PeerOwnerId=peer_owner_id,
                PeerRegion=peer_region
            )['VpcPeeringConnection']['VpcPeeringConnectionId']
        config['peering_connection_id'] = peering_id
    except (botocore.exceptions.ClientError, botocore.exceptions.ParamValidationError) as exc:
        logger.error("Exception happened during create vpc peering connection: %s", exc)
        sys.exit(1)


def accept_peering_connection(logger, config):
    peering_id = config['peering_connection_id']

    logger.info("Approving from accepter(%s) side for peering %s.", config['accepter']['acc'], peering_id)
    retry_count = RETRY_COUNT
    while True:
        try:
            config['accepter']['ec2_client'].accept_vpc_peering_connection(
                VpcPeeringConnectionId=peering_id
            )
            break
        except botocore.exceptions.ClientError as exc:
            message = exc.response['Error']['Code']
            if 'InvalidVpcPeeringConnectionID.NotFound' in message:
                logger.debug(f"Acceptor doesn't know the peering ID yet. Sleeping for {RETRY_SLEEP} seconds")
                sleep(RETRY_SLEEP)
                if retry_count <= 0:
                    logger.error("Retried %d times and the accepter(%s) still does not know about"
                                 " the vpc peering id %s. Something is wrong.",
                                 config['accepter']['acc'], peering_id)
                    sys.exit(1)
                retry_count -= 1
            else:
                logger.error("Exception happened during accepting %s : %s", peering_id, exc)
                sys.exit(1)


def configure_routing(logger, config):
    logger.info("Setting up routing")
    for party, setup in config['desired'].items():
        for route_table, target_subnets in setup.items():
            for target_subnet in target_subnets:
                logger.warning("Add routing item in %s for cidr %s, destination %s",
                               route_table, target_subnet.cidr_block, config['peering_connection_id'])
                try:
                    response = config[party]['ec2_client'].create_route(
                        RouteTableId=route_table,
                        DestinationCidrBlock=target_subnet.cidr_block,
                        VpcPeeringConnectionId=config['peering_connection_id']
                    )
                    if not response:
                        logger.error("Failed to update route table '%s' with destination cidr '%s'",
                                     route_table, target_subnet.cidr_block)
                except botocore.exceptions.ClientError as exc:
                    logger.error("Failed to update route table '%s' with destination cidr '%s'. Exception %s",
                                 route_table, target_subnet.cidr_block, exc)


def setup_peering(logger, config):
    """
    Setup peering and configure routing between VPCs
    """
    logger.info("Starting peering setup")

    create_peering_connection(logger, config)
    accept_peering_connection(logger, config)
    configure_routing(logger, config)

    logger.info("Peering setup complete")


def delete_peer(logger, ec2_client, peer, vpc_name):
    logger.info('Tear down peering: %s %s', vpc_name, peer.id)
    try:
        peer.delete()
        while True:  # wait for status in deleted
            try:
                resp = ec2_client.describe_vpc_peering_connections(
                    VpcPeeringConnectionIds=[peer.id]
                )
                if resp['VpcPeeringConnections'][0]['Status']['Code'] == 'deleted':
                    break
                sleep(10)
            except botocore.exceptions.ClientError as exc:
                logger.warning("Failed while waiting for peering connection deletion to complete, error: %s", exc)
                logger.warning("This should be ok. Proceeding")
                break  # if no longer accessible, then still OK to proceed.
    except botocore.exceptions.ClientError as exc:
        logger.warning("Got an exception while trying to delete peer: %s", exc)
        message = exc.response['Error']['Code']
        if 'InvalidStateTransition' in message:
            logger.warning("InvalidStateTransition error caught, this can be ignored")


def delete_routes(logger, peer, route_tables):
    for route_table in route_tables:
        for item in route_table.routes:
            if item.vpc_peering_connection_id is None:  # nothing related to peering.
                continue
            if item.vpc_peering_connection_id == peer.id \
                    or item.vpc_peering_connection_id.startswith('pcx-') \
                    and item.state == 'blackhole':  # here we also clean up
                # possible garbages due to previous vpc peering failure, so in the future
                # there are less possibility in conflicts
                logger.warning('delete item in route: %s, destination %s, cidr %s, state: %s',
                               item.route_table_id, item.vpc_peering_connection_id,
                               item.destination_cidr_block, item.state)
                try:
                    item.delete()
                except botocore.exceptions.ClientError as exc:
                    logger.warning("Got an exception deleting a route: %s", exc)
                    logger.warning("Proceeding")


def cleanup_peering(logger, config):
    """
    Clean up peering and routes.
    """
    logger.info("Cleaning up existing peers.")
    for party in ['requester', 'accepter']:
        for peer in config[party]['existing_peer']:
            delete_peer(logger, config[party]['ec2_client'], peer, config[party]['vpc_name'])
            delete_routes(logger, peer, config[party]['vpc_resource'].route_tables.all())

    logger.info("Peering cleanup complete")


def get_affected_route_tables(logger, vpc_resource, vpc_name, route_table, who):
    all_route_tables = list(vpc_resource.route_tables.all())
    affected_route_tables = filter_by_id_or_prefix(logger,
                                                   all_route_tables,
                                                   route_table,
                                                   vpc_name)

    if not affected_route_tables:
        logger.error("Could not find route table looks like '%s' for '%s'", route_table, who)
        sys.exit(1)

    return affected_route_tables


def get_affected_subnets_or_vpc(logger, vpc_resource, vpc_name, target, who):
    if target:  # if specifies the subnets pattern
        all_dest_subnets = list(vpc_resource.subnets.all())
        affected_subnets_or_vpc = filter_by_id_or_prefix(logger,
                                                         all_dest_subnets,
                                                         target,
                                                         vpc_name)
    else:
        affected_subnets_or_vpc = [vpc_resource]
    if not affected_subnets_or_vpc:
        logger.error("Could not find route table looks like '%s' for '%s'", target, who)
        sys.exit(1)

    return affected_subnets_or_vpc


def get_unrelated_route_destinations(logger, existing_peers, affected_route_tables, account):
    logger.info("Looking for unrelated routes")
    # collect cidr information
    to_be_removed_peer_ids = [p.id for p in existing_peers]

    route_destination_non_related = [
        [(
            r.destination_cidr_block,
            rt.id,
            beautify_routes_dest(r),
            account,
            rt.vpc_id
        )
         for r in rt.routes
         if r.vpc_peering_connection_id is None  # crap, it is for other non-vpc, will keep
         or r.vpc_peering_connection_id not in to_be_removed_peer_ids and r.state != 'blackhole'
         # it is still being consumed by an active vpc peering
        ]
        for rt in affected_route_tables]

    # flatten route_destination_non_related
    route_destination_non_related = reduce(lambda x, y: x + y, route_destination_non_related)

    return route_destination_non_related


def analyse_route_config(logger, config):
    """
    Find out what are the desired routetable->subnet mappings
    """

    logger.info("Analysing route configuration")
    config['desired'] = {}
    route_destination_conflicted = []
    # populate the original config with actual resources with ids.
    for party_from, party_to in [('requester', 'accepter'), ('accepter', 'requester')]:
        if party_from not in config['routes']:
            logger.warning('%s not found in routes', party_from)
            continue

        routes_config = {}
        config['desired'].update({party_from: routes_config})
        for item in config['routes'][party_from]:
            affected_route_tables = get_affected_route_tables(logger,
                                                              config[party_from]['vpc_resource'],
                                                              config[party_from]['vpc_name'],
                                                              item['route_table'],
                                                              party_from)

            affected_subnets_or_vpc = get_affected_subnets_or_vpc(logger,
                                                                  config[party_to]['vpc_resource'],
                                                                  config[party_to]['vpc_name'],
                                                                  item['to'],
                                                                  party_to)

            route_destination_non_related = get_unrelated_route_destinations(logger,
                                                                             config[party_from]['all_existing_peers'],
                                                                             affected_route_tables,
                                                                             config[party_from]['acc'])

            # filter these are in the affected_cidrs
            affected_cidrs = [s.cidr_block for s in affected_subnets_or_vpc]
            route_destination_conflicted += [r for r in route_destination_non_related if r[0] in affected_cidrs]

            for from_route_table in affected_route_tables:
                if from_route_table.id not in routes_config:
                    routes_config[from_route_table.id] = []

                routes_config[from_route_table.id].extend(affected_subnets_or_vpc)

    if route_destination_conflicted:
        for conflict in route_destination_conflicted:
            logger.error(
                "Potential future cidr conflicts in routing. cidr: %s, route_table id %s, currently being used by %s. "
                "Login AWS console for User: %s, VPC: %s to resolve it, then come back and re-run this tool.",
                conflict[0], conflict[1], conflict[2], conflict[3], conflict[4])
        sys.exit(1)
    logger.info("Route configuration analysis complete")


def verify_vpcs(logger, config, root_profile=None, region=DEFAULT_REGION):
    """
    Verify if the config's vpc configuration allows carrying out the next operations.
    If permission does not exist, or cannot identify the only one VPC to operate on both requester and
    accepter VPC, an exception is raised.

    If current configuration conflicts with operation mode, then raise Exception.
    Mode: careful: if existing vpc has peering, then do nothing.
          modest: only create or upgrade from existing peering between the two vpcs. Else exit. (default)
          force: clean whatever peering of both VPCs setting and build peering.

    As a result, the config will be updated.
    """
    logger.info("Verify VPC information...")
    try:
        boto_session = boto3.Session(profile_name=root_profile)
        # current only support assume role. extend them in the future
        for party in ['requester', 'accepter']:
            logger.info(f'Analysing {party}')
            analyse_account(logger, config[party], boto_session, region)

        logger.info("Verify VPC finished")
    except botocore.exceptions.NoCredentialsError:
        logger.error("No AWS credentials supplied")
        sys.exit(1)
    except botocore.exceptions.ProfileNotFound:
        logger.error("AWS profile not found")
        sys.exit(1)

    return config


def construct_role(account, role):
    if not role.startswith('arn'):
        role = f'arn:aws:iam::{account}:role/{role}'

    return {'role': role}


vpc_peering.add_param('-c', '--config', required=True,
                      help='OPTIONAL. Configuration file. If not provided, then this app ignores other'
                           'parameters and simply generate a skeleton of config file. '
                           'Some configuration example can be found at '
                           'https://github.com/rozettatechnology/new-devops/blob/develop/manual/utils/sample.yaml')
vpc_peering.add_param('-f', '--force', default=False, action='store_true',
                      help='OPTIONAL. Use this option to force apply the peering configuration even if there '
                           'is already peering between the VPCs. This is useful when we want to clean up the '
                           'old config and re-establish with the new config. USE WITH CARE. As the new config may '
                           'have less routing config than the old peering, this behavior may cause some '
                           'partial network disconnection between the VPCs.')
vpc_peering.add_param('-a', '--action', choices=['apply', 'delete', 'plan'], required=False, default='apply',
                      help='OPTIONAL. apply: Create or update peering setting to desired configuration.'
                           'delete: Delete the peering between two VPCs.')
vpc_peering.add_param("-r", "--region", help="region to override the settings in profile", default=DEFAULT_REGION)
vpc_peering.add_param("-p", "--profile", help="the default profile if not specified in the config", default=None)


def main():
    vpc_peering.run()
    return 0


if __name__ == '__main__':
    sys.exit(main())
