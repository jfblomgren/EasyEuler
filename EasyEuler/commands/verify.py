import os

import click

from EasyEuler.types import LanguageType, ProblemType
from EasyEuler.utils import verify_solution, get_problem, get_problem_id


@click.command()
@click.option('--language', '-l', type=LanguageType(),
              help='The language of the file(s).')
@click.option('--recursive', '-r', is_flag=True,
              help='Verify files in specified directory paths.')
@click.option('--time', '-t', is_flag=True,
              help='Time the execution of files.')
@click.option('--errors', '-e', is_flag=True,
              help='Show errors.')
@click.argument('path', type=click.Path(exists=True, readable=True), nargs=-1)
def cli(path, language, recursive, time, errors):
    """
    Verify the solution to a problem.

    Runs the appropriate command for a language (specified in the configuration
    file) with the file path(s) as arguments.

    If the LANGUAGE option isn't specified, it will be identified based on the
    file extension.

    Similarly, the problem ID will be identified based on the file name.

    """

    for path_ in path:
        if os.path.isdir(path_):
            if recursive:
                validate_directory_files(path_, time, language, errors)
            else:
                click.echo('Skipping %s because it is a directory and '
                           '--recursive was not specified' %
                           click.format_filename(path_))
            continue

        validate_file(path_, time, language, errors)


def validate_directory_files(path, time_execution, language, errors):
    for root, directories, file_names in os.walk(path):
        for file_name in file_names:
            validate_file(os.path.join(root, file_name), time_execution, language, errors)


def validate_file(path, time_execution, language, errors):
    problem_id = get_problem_id(path)
    if problem_id is None or get_problem(problem_id) is None:
        click.echo('Skipping %s because it does not contain '
                   'a valid problem ID' % click.format_filename(path))
        return

    click.echo('Checking output of %s: ' % click.format_filename(path), nl=False)
    status, output, execution_time = verify_solution(path, time_execution,
                                                     problem_id, language)

    click.secho({'C': output, 'I': output or '[no output]',
                 'E': '\n%s' % output if errors else '[error]'}[status],
                fg='red' if status in ('I', 'E') else 'green')

    if execution_time is not None:
        click.secho('CPU times - user: {user}, system: {system}, total: {total}\n'
                    'Wall time: {wall}\n'.format(**execution_time), fg='cyan')
