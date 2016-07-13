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
        generate_all_resources(path)
    else:
        generate_problem_resources(problem, path)


def generate_problem_resources(problem, path):
    if 'resources' not in problem:
        sys.exit('Problem %s has no resource files' % problem['id'])

    for filename in problem['resources']:
        shutil.copy('%s/resources/%s' % (data.DATA_PATH, filename), path)
        click.echo('Created %s at path %s' % (filename, path))


def generate_all_resources(path):
    for problem in data.problems:
        if 'resources' in problem:
            generate_problem_resources(problem, path)
