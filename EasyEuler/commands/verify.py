import os
import re
import sys
import math
import subprocess
import time

import click

from EasyEuler.types import LanguageType
from EasyEuler.utils import get_problem, get_language


PROBLEM_ID_REGEX = re.compile(r'\D*([1-9]\d{0,2}).*')


@click.command()
@click.option('--language', '-l', type=LanguageType(),
              help='The language of the file(s).')
@click.option('--recursive', '-r', is_flag=True,
              help='Verify files in specified directory paths.')
@click.option('--time', '-t', is_flag=True,
              help='Time the execution of files.')
@click.option('--errors', '-e', is_flag=True,
              help='Show errors.')
@click.argument('paths', type=click.Path(exists=True, readable=True), nargs=-1,
                metavar='[PATH]...')
def cli(paths, language, recursive, time, errors):
    """
    Verify the solution to a problem.

    Runs the appropriate command for a language (specified in the configuration
    file) with the file path(s) as arguments.

    If the LANGUAGE option isn't specified, it will be identified based on the
    file extension.

    Similarly, the problem ID will be identified based on the file name.

    """

    for path in paths:
        if os.path.isdir(path):
            if recursive:
                validate_directory_files(path, time, language, errors)
            else:
                click.echo('Skipping %s because it is a directory and '
                           '--recursive was not specified' %
                           click.format_filename(path))
            continue

        validate_file(path, time, language, errors)


def validate_directory_files(path, time_execution, language, errors):
    for root, directories, file_names in os.walk(path):
        for file_name in file_names:
            validate_file(os.path.join(root, file_name), time_execution,
                          language, errors)


def validate_file(path, time_execution, language, errors):
    problem_id = get_problem_id(path)
    if problem_id is None or get_problem(problem_id) is None:
        click.echo('Skipping %s because it does not contain '
                   'a valid problem ID' % click.format_filename(path))
        return
    problem = get_problem(problem_id)

    if language is None:
        file_extension = os.path.splitext(path)[1].replace('.', '')
        language = get_language(file_extension, 'extension')

    verify_solution(path, time_execution, problem, language, errors)


def get_problem_id(path):
    problem_id = PROBLEM_ID_REGEX.findall(path)
    return int(problem_id[0]) if len(problem_id) > 0 else None


def verify_solution(path, time_execution, problem, language, errors):
    command = './{path}' if language is None else language['command']

    click.echo('Checking output of %s: ' % click.format_filename(path), nl=False)

    process, execution_time = execute_process(command.format(path=path),
                                              time_execution)

    if process.returncode != 0:
        output = str(process.stderr, encoding='UTF-8')
        click.secho('\n%s' % output if errors else '[error]', fg='red')
    else:
        output = str(process.stdout, encoding='UTF-8').replace('\n', '')
        click.secho(output or '[no output]',
                    fg='green' if output == problem['answer'] else 'red')

    if time_execution:
        if 'user' in execution_time:
            execution_time_msg = 'CPU times - user: {user}, ' \
                                 'system: {system}, total: {total}\n' \
                                 'Wall time: {wall}\n'
        else:
            execution_time_msg = 'Time: {wall}\n'
        click.secho(execution_time_msg.format(**execution_time), fg='cyan')


def execute_process(command, time_execution):
    if time_execution:
        start_time = get_time()
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        end_time = get_time()

        execution_time = {key: format_time(end_time[key] - start_time[key])
                          for key in end_time}
    else:
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        execution_time = None

    return process, execution_time


try:
    import resource
    def get_time():
        rs = resource.getrusage(resource.RUSAGE_CHILDREN)
        return {'user': rs.ru_utime, 'system': rs.ru_stime,
                'total': rs.ru_stime + rs.ru_utime, 'wall': time.time()}
except ImportError:
    # The resource module only exists on UNIX.
    # This is a different platform, so we can't 
    # provide user and system times.
    def get_time():
        return {'wall': time.time()}


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
