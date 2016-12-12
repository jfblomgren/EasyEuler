import math
import os
import re
import subprocess
import sys
import time

import click

from EasyEuler import data
from EasyEuler.types import LanguageType


PROBLEM_ID_REGEX = re.compile(r'\D*([1-9]\d{0,2}).*')
STAGES = ('build', 'execute', 'cleanup')


@click.command()
@click.option('--time', '-t', is_flag=True,
              help='Time the execution of files.')
@click.option('--errors', '-e', is_flag=True,
              help='Show errors.')
@click.option('--recursive', '-r', is_flag=True,
              help='Verify files in specified directory paths.')
@click.option('--language', '-l', type=LanguageType(),
              help='The language of the file(s).')
@click.argument('paths', type=click.Path(exists=True, readable=True), nargs=-1,
                metavar='[PATH]...')
def cli(paths, language, time, errors, recursive):
    """
    Verify the solution to a problem.

    Runs the appropriate command for a language (specified in the
    configuration file) with the file path(s) as arguments.

    If the LANGUAGE option isn't specified, it will be identified based
    on the file extension. Similarly, the problem ID will be identified
    based on the file name.

    """

    for path in paths:
        if os.path.isdir(path):
            if recursive:
                validate_directory(path, language, time, errors)
            else:
                click.echo('Skipping %s because it is a directory '
                           'and --recursive was not specified' %
                           click.format_filename(path))
        else:
            validate_file(path, language, time, errors)


def validate_directory(path, language, time_execution, show_errors):
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            validate_file(file_path, language, time_execution, show_errors)


def validate_file(path, language, time_execution, show_errors):
    problem = get_problem_from_path(path)
    if problem is None:
        click.echo('Skipping %s because it does not contain '
                   'a valid problem ID' % click.format_filename(path))
        return

    if language is None:
        language = get_language_from_path(path) or {}

    click.echo('Checking output of %s: ' % click.format_filename(path),
               nl=False)
    result = verify_solution(path, language, time_execution, problem)
    print_result(result, show_errors, time_execution)


def print_result(result, show_errors, show_time):
    if result['error'] != 'none':
        if show_errors:
            error_message = result[result['error']]['output']
        else:
            error_message = '[error during %s]' % result['error']
        click.secho('\n%s' % error_message, fg='red')
        return

    click.secho(result['execute']['output'] or '[no output]',
                fg='green' if result['correct'] else 'red')

    if show_time:
        print_execution_time(result['execute']['execution_time'])


def print_execution_time(execution_time):
    if 'user' in execution_time:
        execution_time_msg = 'CPU times - user: {user}, '         \
                             'system: {system}, total: {total}\n' \
                             'Wall time: {wall}\n'
    else:
        execution_time_msg = 'Time: {wall}\n'
    click.secho(execution_time_msg.format(**execution_time), fg='cyan')


def get_problem_from_path(path):
    problem_id = get_problem_id_from_path(path)
    if problem_id is None:
        return None
    return data.problems.get(problem_id)


def get_language_from_path(path):
    file_extension = os.path.splitext(path)[1].replace('.', '')
    return data.config.get_language('extension', file_extension)


def get_problem_id_from_path(path):
    problem_id = PROBLEM_ID_REGEX.findall(path)
    return int(problem_id[0]) if len(problem_id) > 0 else None


def verify_solution(path, language, time_execution, problem):
    commands = get_commands(path, language)
    result = {'error': 'none'}

    for stage in STAGES:
        if commands[stage] is None:
            continue

        if stage == 'execute':
            result[stage] = execute_process(commands[stage], time_execution)
            result['correct'] = result[stage]['output'] == problem['answer']
        else:
            result[stage] = execute_process(commands[stage], False)

        if result[stage]['error']:
            result['error'] = stage
            break

    return result


def get_process_output(process):
    if process.returncode != 0:
        return str(process.stderr, encoding='UTF-8'), True
    return str(process.stdout, encoding='UTF-8').rstrip(), False


def get_commands(path, language):
    commands = {'build': None, 'cleanup': None}
    commands['execute'] = language.get('execute', './{path}').format(path=path)

    if 'build' in language:
        commands['build'] = language['build'].format(path=path)
    if 'cleanup' in language:
        commands['cleanup'] = language['cleanup'].format(path=path)

    return commands


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

    output, error = get_process_output(process)
    return {'output': output, 'error': error, 'execution_time': execution_time}


try:
    import resource

    def get_time():
        rs = resource.getrusage(resource.RUSAGE_CHILDREN)
        return {'user': rs.ru_utime, 'system': rs.ru_stime,
                'total': rs.ru_stime + rs.ru_utime, 'wall': time.time()}
except ImportError:
    # The resource module only exists on Unix-based platforms.
    # This is a different platform, so we can't provide user
    # and system times.
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
