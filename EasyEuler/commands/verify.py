import os
import sys
import math

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
    execution_time = {key: format_time(value)
                      for key, value in execution_time.items()}

    click.secho({'C': output, 'I': output or '[no output]',
                 'E': '\n%s' % output if errors else '[error]'}[status],
                fg='red' if status in ('I', 'E') else 'green')

    if execution_time is not None:
        click.secho('CPU times - user: {user}, system: {system}, total: {total}\n'
                    'Wall time: {wall}\n'.format(**execution_time), fg='cyan')


def format_long_time(timespan):
    """
    Formats a long timespan in a human-readable form with a
    precision of a 100th of a second.

    """

    formatted_time = []
    units = (('d', 24 * 60 * 60), ('h', 60 * 60), ('m', 60), ('s', 1))

    for unit, length in units:
        value = int(timespan / length)

        if value > 0:
            timespan %= length
            formatted_time.append('%i%s' % (value, unit))

        if timespan < 1:
            break

    return ' '.join(formatted_time)


def format_short_time(timespan):
    """
    Formats a short timespan in a human-readable form with a
    precision of a billionth of a second.

    """

    scaling = (1, 1e3, 1e6, 1e9)
    units = ['s', 'ms', 'us', 'ns']

    # Attempt to change 'u' to the micro symbol if it's supported.
    if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding:
        try:
            '\xb5'.encode(sys.stdout.encoding)
            units[2] = '\xb5s'
        except UnicodeEncodeError:
            pass

    if timespan > 0:
        order = min(-int(math.floor(math.log10(timespan)) // 3), 3)
    else:
        order = 3

    return '%.*g%s' % (3, timespan * scaling[order], units[order])


def format_time(timespan):
    """
    Formats a timespan in a human-readable form.
    Courtesy of IPython.

    """

    if timespan >= 60:
        # If the time is greater than one minute,
        # precision is reduced to a 100th of a second.
        return format_long_time(timespan)
    return format_short_time(timespan)
