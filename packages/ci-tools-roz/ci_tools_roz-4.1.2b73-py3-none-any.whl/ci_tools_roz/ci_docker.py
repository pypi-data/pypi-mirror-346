#! /usr/bin/env python3
# pylint: disable=logging-fstring-interpolation,too-many-locals,fixme
import os
import sys
import argparse
import textwrap
import pathlib
import base64
import logging
import docker
import yaml
import boto3
from ci_tools.version import get_package_version, get_jenkins_pipeline, git_details_v2

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)


# This is a PoC for conditionally building and tagging docker images.
# There may be an upcoming issue that image digests get a lot of tags as they dont changes for every githash change.
# AWS has a 1000  tag limit per container digest

class IllegalArgumentError(ValueError):
    pass


# pylint: disable=too-few-public-methods
class EcrImage:
    def __init__(self, ecr: str = None, repo: str = None, tag: str = None, version_string: str = None):
        if version_string:
            if any([ecr, repo, tag]):
                raise IllegalArgumentError('EcrImage:version_string is exclusive with other args')
            self._parse_version_string(version_string)
        else:
            self.ecr = ecr
            self.repo = repo
            self.tag = tag

    def __repr__(self):
        name = ''
        if self.ecr:
            name += f'{self.ecr}/'
        if self.repo:
            name += self.repo
        if self.tag:
            name += f':{self.tag}'

        return name

    def _parse_version_string(self, version_string):
        '''
        :param version_string: [<ecr>/][<image>][:<version>]
        '''

        self.ecr = None
        self.repo = None
        self.tag = None

        parts = version_string.split('/', 1)
        if len(parts) == 2:
            self.ecr = parts[0]
            version_string = parts[1]

        parts2 = version_string.split(':', 1)
        self.repo = parts2[0] or None  # avoid empty string ''

        if len(parts2) == 2:
            self.tag = parts2[1]


def build(aws_region, rel_path,  target_image, autovivify=False):
    '''
    NB githash is used as the "primary" tag of the image.
    :param aws_region:
    :param rel_path:      to the dockerfile etc
    :param target_image:  NB tag field is "semvar" version
    :param autovivify:    auto create the ECR if missing
    :return:
    '''
    is_dirty, githash, _, _ = git_details_v2(path=rel_path)
    rzt_semvar_tag = get_package_version(target_image.tag, path=rel_path).replace('+', '_')

    target_repo_by_git_hash = EcrImage(target_image.ecr, target_image.repo, githash)
    image_by_githash = f'{target_image.repo}:{githash}'

    image = ecr_get_image_by_tag(aws_region, target_repo_by_git_hash.repo, target_repo_by_git_hash.tag,
                                 autovivify=autovivify)
    if image:
        logger.info(f'{target_repo_by_git_hash} exists. No build needed.')
    else:
        logger.info(f'Building docker image for: {target_repo_by_git_hash}')
        try:
            docker_client = docker.from_env()
        except Exception as e:  # pylint: disable=broad-except
            logger.error('Check that Docker is running')
            raise docker.errors.DockerException('Docker is not running ?', e)

        response = docker_client.images.build(path=rel_path, tag=[image_by_githash],
                                              labels={'version': target_image.tag, 'githash': githash})
        logger.info(f'built image: {response[0]}')
        for line in response[1]:
            logger.info(line.get('stream', line))

        if is_dirty:
            logger.warning('Repo is dirty not publishing')
            return

        # Publish  the image with the minimal githash tag
        image_id = docker_client.images.get(image_by_githash)
        image_id.tag(repository=f'{target_repo_by_git_hash}', tag=githash)
        docker_push(aws_region, docker_client, [f'{target_image.ecr}/{image_by_githash}'])

    if is_dirty:
        logger.warning('Repo is dirty not tagging')
        return

    tags = [f'{rzt_semvar_tag}']  # posit non 'release'
    if get_jenkins_pipeline() == 'release':
        (major, minor, patch) = target_image.tag.split('.')
        tags = [f'{major}', f'{major}.{minor}', f'{major}.{minor}.{patch}']

    update_soft_tags(aws_region, target_repo_by_git_hash, tags)


def promote(aws_region, source_repo, target_repo, autovivify=False):
    '''
    :param aws_region:
    :param source_repo:
    :param target_repo:
    :param autovivify:  auto create the ECR if missing

    :return:
    '''

    image = ecr_get_image_by_tag(aws_region, target_repo.repo, target_repo.tag, autovivify=autovivify)
    if image:
        logger.info(f'{target_repo} exists. No promotion needed.')
    else:
        logger.info(f'Promoting from:{source_repo} to {target_repo}')
        try:
            docker_client = docker.from_env()
        except Exception as e:  # pylint: disable=broad-except
            logger.error('Check that Docker is running')
            raise docker.errors.DockerException('Docker is not running ?', e)

        pull_region = source_repo.ecr.split('.')[3]
        image = docker_pull(pull_region, docker_client, f'{source_repo.ecr}/{source_repo.repo}',
                            source_repo.tag)
        if not image:
            logger.error(f'Can not find image to promote: {source_repo}')
            return

        image.tag(repository=f'{target_repo.ecr}/{target_repo.repo}', tag=target_repo.tag)
        docker_push(aws_region, docker_client,
                    [f'{target_repo.ecr}/{target_repo.repo}:{target_repo.tag}'])

    (major, minor, _) = target_repo.tag.split('.')
    tags = [f'{major}', f'{major}.{minor}']

    update_soft_tags(aws_region, target_repo, tags)


def docker_push(aws_region, docker_client, tags):
    '''
    :param aws_region: for ECR
    :param docker_client:  references the image to push
    :param tags: list of tags to push
    :return:
    '''
    ecr_client = boto3.client('ecr', region_name=aws_region)

    # This is the equivalent of the aws ecr login
    response = ecr_client.get_authorization_token()
    token = response['authorizationData'][0]['authorizationToken']
    token = base64.b64decode(token).decode()
    username, password = token.split(':')
    auth_config = {'username': username, 'password': password}

    for tag in tags:
        for line in docker_client.images.push(tag, auth_config=auth_config, stream=True, decode=True):
            logger.info(line)


def docker_pull(region, docker_client, repository, tag):
    logger.info('Pulling: {region} {repository}:{tag}')

    ecr_client = boto3.client('ecr', region_name=region)

    # This is the equivalent of the aws ecr login
    response = ecr_client.get_authorization_token()
    token = response['authorizationData'][0]['authorizationToken']
    token = base64.b64decode(token).decode()
    username, password = token.split(':')
    auth_config = {'username': username, 'password': password}

    try:
        image = docker_client.images.pull(repository, tag=tag, auth_config=auth_config)
        return image
    except Exception as e:  # pylint: disable=broad-except
        logger.error(f'docker_pull({region}, {repository}, {tag}) failed. %s', e.explanation)

    return None


def ecr_get_image_by_tag(region, repo, tag, autovivify=False):
    """
    Gets ECR metadata by tag. No image pulling
    :param region:
    :param repo:
    :param tag: to search for
    :param autovivify:   auto create the ECR if non existant
    :return: image if found
    """
    ecr_client = boto3.client('ecr', region_name=region)

    try:
        response = ecr_client.batch_get_image(
            repositoryName=repo,
            imageIds=[{'imageTag': tag}]
        )
        if response['images']:
            return response['images'][0]

        failures = response.get('failures')
        logger.info(failures)
    except ecr_client.exceptions.RepositoryNotFoundException as error:
        logger.error(f'{region}:{repo} Not found {error}')
        if autovivify:
            response = ecr_client.create_repository(
                repositoryName=repo,
                tags=[{'Key': 'Info', 'Value': 'autovivified'}],
                imageScanningConfiguration={'scanOnPush': True}
            )
            logger.info('Created ECR: %s', response['repository']['repositoryArn'])

    return None


def ecr_tag_image(region, repo, manifest, new_tag):
    ecr_client = boto3.client('ecr', region_name=region)

    try:
        ecr_client.put_image(
            repositoryName=repo,
            imageManifest=manifest,
            imageTag=new_tag
        )
        logger.info(f'ecr tagged: {region}:{repo}/{new_tag}')
    except ecr_client.exceptions.ImageAlreadyExistsException:
        logger.warning(f'ecr_tag_image:{region}:{repo}/{new_tag} already exists')


def update_soft_tags(aws_region, target_repo, tags):
    image_name = target_repo.repo
    image = ecr_get_image_by_tag(aws_region, image_name, target_repo.tag)

    # Do we need to add or bump soft tags ?
    for tag in tags:
        image_by_tag = ecr_get_image_by_tag(aws_region, image_name, tag)
        if not image_by_tag:
            ecr_tag_image(aws_region, image_name, image['imageManifest'], tag)
        elif image_by_tag['imageId']['imageDigest'] != image['imageId']['imageDigest']:
            logger.info(f'{target_repo} bumping tag:{tag} from %s to %s',
                        image_by_tag['imageId']['imageDigest'],  image['imageId']['imageDigest'])

            ecr_tag_image(aws_region, image_name, image['imageManifest'], tag)
        else:
            logger.info(f'{target_repo} already tagged with {tag}')


def read_config(file_path=None):
    with open(file_path) as f:
        return yaml.safe_load(f)


def main():
    """
    Either build/deploy to ECR
    - based on githash
     or promote from a source ECR
    - basesd on version

    Promotion is done via version. We assume that correct version has already been created.
    :return:
    """
    parser = argparse.ArgumentParser(description='Build or Promote Docker image',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-r', '--region', metavar='<region>',
                        help='Region to Build/Promote the image',
                        required=True)
    parser.add_argument('-a', '--autocreateecr', default=False, action="store_true",
                        help='if target ECR doesnt exist then create')

    subparsers = parser.add_subparsers(dest='command', metavar='')
    parser_build = subparsers.add_parser('build', help=textwrap.dedent('''
        For a Build the image name is taken from last part of <path>. The ECR is from the current AWS environment
        - The image is tagged and labelled with the githash related to the path.
        - The path contains a Dockerfile, source for the image and a config.yaml containing:
            version: <semvar>    # e.g. 1.0.1
        - The image is also tagged with version: X.Y.Z and 'soft tags': X and  X.Y
                                        '''))
    parser_build.add_argument('-d', '--dir', metavar='<path>', required=True,
                              help='Build and publish the image from <path> to the ECR of the current AWS environment')

    parser_promote = subparsers.add_parser('promote', help=textwrap.dedent('''
        Promote the image:version from the source_ecr to target_ecr.
        - A minimal source definition is a source_ecr. The image name comes from the target.
        - If source image_name is specified then is could be used say to specify an <env> based image name.
          e.g. promote from dev_image to qa_image in same ECR.
        - A minimal target is just an image:version. The ECR is taken from the current AWS environment.
        - The version is taken from target image.
                                     '''))
    parser_promote.add_argument('-s', '--source', metavar='<source ecr>[/<source image>]', required=True,
                                help='Promote the image from the given ECR.')
    parser_promote.add_argument('-t', '--target', metavar='[<target ecr>/]<target image>:<version>', required=True,
                                help='Promote the image to given ECR. '
                                'Default is to promote to same image/version in ecr of AWS_PROFILE and <region>')

    args = parser.parse_args()

    logger.setLevel(logging.INFO)

    aws_region = args.region

    aws_account_id = boto3.client('sts').get_caller_identity()['Account']

    if args.command == 'build':
        rel_path = args.dir
        image_dir = pathlib.Path.cwd() / rel_path
        config = read_config(image_dir / 'config.yaml')
        target_image = EcrImage(f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com',
                                image_dir.name,
                                config['version'])

        build(aws_region, rel_path, target_image, autovivify=args.autocreateecr)

    elif args.command == 'promote':
        if '/' not in args.source:  # Edge case minimal source should be an 'ecr'' (not a 'repo')
            args.source += '/'
        source_repo = EcrImage(version_string=args.source)
        target_repo = EcrImage(version_string=args.target)

        # Handle the default fields between source and target.
        if not source_repo.repo:
            source_repo.repo = target_repo.repo
        if not source_repo.tag:
            source_repo.tag = target_repo.tag
        if not target_repo.ecr:
            target_repo.ecr = f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com'

        promote(aws_region, source_repo, target_repo, autovivify=args.autocreateecr)


if __name__ == '__main__':
    main()
