import sys
import resource
import os

import click

from .utils import write_to_file, get_problem, get_problem_id, verify_solution
from .types import ProblemType, LanguageType


commands = click.Group()


@commands.command()
@click.option('--path', '-p', type=click.Path())
@click.option('--overwrite', '-o', is_flag=True)
@click.argument('problem', type=ProblemType())
@click.argument('language', type=LanguageType(),
                required=False, default='python')
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
@click.option('--language', '-l', type=LanguageType())
@click.option('--recursive', '-r', is_flag=True)
@click.option('--time', '-t', is_flag=True)
@click.argument('path', type=click.Path(exists=True, readable=True), nargs=-1)
def verify(path, language, recursive, time):
    for path_ in path:
        if os.path.isdir(path_):
            if recursive:
                process_dir(path_, time, language)
            else:
                click.echo('Skipping %s because it is a directory and ' \
                           '--recursive was not specified' %
                           click.format_filename(path_))
            continue

        validate_file(path_, time, language)


def process_dir(path, time_execution, language):
    for root, directories, file_names in os.walk(path):
        for file_name in file_names:
            validate_file(os.path.join(root, file_name), time_execution, language)


def validate_file(path, time_execution, language):
    problem_id = get_problem_id(path)
    if problem_id is None or get_problem(problem_id) is None:
        click.echo('Skipping %s because it does not contain ' \
                   'a valid problem ID' % click.format_filename(path))
        return

    status, output, execution_time = verify_solution(path, time_execution,
                                                     problem_id, language)

    click.echo('Checking output of %s: %s' % (click.format_filename(path),
                                              output))
    click.echo({'C': 'Correct', 'I': 'Incorrect', 'E': 'Error'}[status])
    if execution_time is not None:
        click.echo('CPU times: user: {}, system: {}, total: {}'.format(*execution_time[1:]))
        click.echo('Wall time: %s' % execution_time[0])
