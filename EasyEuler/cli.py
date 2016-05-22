import sys

import click

from .utils import write_to_file, get_problem


@click.group()
def commands():
    pass


@click.command()
@click.argument('problem_id', type=click.IntRange(1, None))
@click.argument('language', required=False, default='python')
def generate(problem_id, language):
    problem = get_problem(problem_id)

    if problem is None:
        sys.exit('Problem %d does not exist' % problem_id)

    file_name = write_to_file(problem, language)
    click.echo('Written to file %s' % file_name)

commands.add_command(generate)
