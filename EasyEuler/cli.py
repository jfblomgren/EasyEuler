import sys
import os

import click

from .utils import write_to_file, get_problem, get_problem_id, verify_solution
from .types import ProblemType


commands = click.Group()


@commands.command()
@click.option('--path', '-p', type=click.Path())
@click.option('--overwrite', '-o', is_flag=True)
@click.argument('problem', type=ProblemType())
@click.argument('language', required=False, default='python')
def generate(problem, language, path, overwrite):
    try:
        path, success = write_to_file(problem, language, path, overwrite)
    except (FileNotFoundError, PermissionError) as e:
        sys.exit('An exception occurred: %s' % e)

    if not success:
        sys.exit('%s already exists. Use the --overwrite flag to overwrite it' %
                 click.format_filename(path))

    click.echo('Written to %s' % click.format_filename(path))


@commands.command()
@click.option('--language', '-l')
@click.argument('path', type=click.Path(exists=True, readable=True), nargs=-1)
def verify(path, language):
    for path_ in path:
        valid, status, output = process_path(path_, language)
        if not valid:
            continue

        click.echo('Checking output of %s: %s' % (click.format_filename(path_),
                                                  output))
        click.echo({'C': 'Correct', 'I': 'Incorrect', 'E': 'Error'}[status])


def process_path(path, language):
    if os.path.isdir(path):
        click.echo('Skipping %s because it is a directory' %
                   click.format_filename(path))
        return False, None, None

    problem_id = get_problem_id(path)
    if problem_id is None or get_problem(problem_id) is None:
        click.echo('Skipping %s because it does not contain ' \
                   'a valid problem ID' % click.format_filename(path))
        return False, None, None

    status, output = verify_solution(path, problem_id, language)
    return True, status, output
