import os
import sys
import shutil

import click

from EasyEuler import data
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

    If the PROBLEM argument isn't specified, all resources will be generated.

    """

    if problem is None:
        resources = os.listdir('%s/resources' % data.DATA_PATH)
    else:
        if 'resources' not in problem:
            sys.exit('Problem %s has no resource files' % problem['id'])
        resources = problem['resources']

    if len(resources) > 1:
        if os.path.exists(path) and not os.path.isdir(path):
            sys.exit('%s needs to be a directory to '
                     'create multiple resource files' % path)
        os.mkdir(path)

    for resource in resources:
        shutil.copy('%s/resources/%s' % (data.DATA_PATH, resource), path)
        click.echo('Created %s at path %s' % (resource, path))
