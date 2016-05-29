import sys
import glob

import click

from .utils import write_to_file, get_problem, verify_solution
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
# TODO: Find a way to avoid name collision with all function from stdlib
@click.option('--all_', '-a', is_flag=True)
@click.option('--recursive', '-r', is_flag=True)
@click.option('--language', '-l')
@click.argument('path')
def verify(path, all_, recursive, language):
    # TODO: Fix directories counting as a path
    # Only count actual files as paths
    # Possibly create util function
    # http://stackoverflow.com/a/2186565/4863420
    if all_:
        paths = glob.glob(path, recursive=recursive)
    else:
        paths = [glob.glob(path, recursive=recursive)[0]]

    if not len(paths) > 0:
        sys.exit('No files matching the pattern "%s" were found' % path)

    for path_ in paths:
        status, output = verify_solution(path_, language=language)
        click.echo('Checking output of %s: %s' % (path_, output))
        click.echo({'C': 'Correct', 'I': 'Incorrect', 'E': 'Error'}[status])
