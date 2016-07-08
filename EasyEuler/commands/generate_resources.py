import sys

import click

from EasyEuler.types import ProblemType
from EasyEuler.utils import generate_all_resources, generate_problem_resources


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
        if 'resources' not in problem:
            sys.exit('Problem %s has no resource files' % problem['id'])
        generate_problem_resources(problem, path)
