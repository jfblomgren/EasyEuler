import os
import shutil
import sys

import click

from EasyEuler import paths
from EasyEuler.types import ProblemType


@click.command('generate-resources')
@click.option('--path', '-p', type=click.Path(writable=True, readable=False),
              default='.', help='Creates the file(s) at PATH.')
@click.argument('problem', type=ProblemType(), required=False)
def cli(problem, path):
    """
    Generate the resource files for problems.

    These resources are either images - serving as helpful illustrations -
    or text files containing specific data - referenced in the problem.

    If the PROBLEM argument isn't specified, all resources will be
    generated.

    """

    if problem is None:
        resources = os.listdir('%s/resources' % paths.DATA)
    else:
        if 'resources' not in problem:
            sys.exit('Problem %s has no resource files' % problem['id'])
        resources = problem['resources']

    generate_resources(resources, path)


def generate_resources(resources, path):
    if len(resources) > 1 and not os.path.isdir(path):
        if os.path.exists(path):
            sys.exit('%s needs to be a directory to create multiple '
                     'resource files' % click.format_filename(path))
        os.mkdir(path)

    for resource in resources:
        if len(resources) > 1 or os.path.isdir(path):
            resource_path = '%s/%s' % (path, resource)
        else:
            resource_path = path

        if os.path.exists(resource_path) and not \
           click.confirm('%s already exists. Do you want to overwrite it?' %
                         click.format_filename(resource_path)):
            continue

        shutil.copy('%s/resources/%s' % (paths.DATA, resource), path)
        click.echo('Created %s at path %s' % (resource,
                                              click.format_filename(path)))
