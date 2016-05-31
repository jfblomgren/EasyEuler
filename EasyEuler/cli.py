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
        if os.path.isdir(path_):
            click.echo('Skipping %s because it is a directory' %
                       click.format_filename(path_))
            continue

        problem_id = get_problem_id(path_)
        if problem_id is None or get_problem(problem_id) is None:
            click.echo('Skipping %s because because it does not contain ' \
                       'a valid problem ID' % click.format_filename(path_))
            continue

        status, output = verify_solution(path_, problem_id, language)

        click.echo('Checking output of %s: %s' % (click.format_filename(path_),
                                                  output))
        click.echo({'C': 'Correct', 'I': 'Incorrect', 'E': 'Error'}[status])
