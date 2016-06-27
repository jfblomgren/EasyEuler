import sys
import resource
import os

import click

from .utils import (write_to_file, get_problem, get_problem_id, verify_solution,
                    generate_problem_resources, generate_all_resources)
from .types import ProblemType, LanguageType


commands = click.Group()


@commands.command()
@click.option('--path', '-p', type=click.Path(),
              help='Writes the file to PATH.')
@click.option('--overwrite', '-o', is_flag=True,
              help='Overwrite the file if it already exists.')
@click.argument('problem', type=ProblemType())
@click.argument('language', type=LanguageType(),
                required=False, default='python')
def create(problem, language, path, overwrite):
    """
    Create the file for a problem.

    Simply specify a valid problem ID and the file will be created at
    euler_<id>.<extension> (if the PATH option isn't specified).

    Optionally, the LANGUAGE argument can be specified, which will then be used
    to identify an appropriate template for the file.

    """

    try:
        path, success = write_to_file(problem, language, path, overwrite)
    except (FileNotFoundError, PermissionError) as e:
        sys.exit('An exception occurred: %s' % e)

    if not success:
        sys.exit('%s already exists. Use the --overwrite flag to overwrite it' %
                 click.format_filename(path))

    click.echo('Written to %s' % click.format_filename(path))


@commands.command()
@click.option('--language', '-l', type=LanguageType(),
              help='The language of the file(s).')
@click.option('--recursive', '-r', is_flag=True,
              help='Verify files in specified directory paths.')
@click.option('--time', '-t', is_flag=True,
              help='Time the execution of files.')
@click.option('--errors', '-e', is_flag=True,
              help='Show errors.')
@click.argument('path', type=click.Path(exists=True, readable=True), nargs=-1)
def verify(path, language, recursive, time, errors):
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
                click.echo('Skipping %s because it is a directory and ' \
                           '--recursive was not specified' %
                           click.format_filename(path_))
            continue

        validate_file(path_, time, language, errors)


@commands.command('generate-resources')
@click.option('--path', '-p', type=click.Path(), default='.',
              help='Creates the file(s) at PATH.')
@click.argument('problem', type=ProblemType(), required=False)
def generate_resources(problem, path):
    """
    Generate the resource files for problems.

    These resources are either images - serving as helpful illustrations -
    or text files - containing specific data - referenced in the problem.

    If the PROBLEM argument isn't specified, all resources will be generated.

    """

    if problem is None:
        generate_all_resources(path)
    else:
        if 'resources' not in problem:
            sys.exit('Problem %s has no resource files' % problem['id'])
        generate_problem_resources(problem, path)


def validate_directory_files(path, time_execution, language, errors):
    for root, directories, file_names in os.walk(path):
        for file_name in file_names:
            validate_file(os.path.join(root, file_name), time_execution, language, errors)


def validate_file(path, time_execution, language, errors):
    problem_id = get_problem_id(path)
    if problem_id is None or get_problem(problem_id) is None:
        click.echo('Skipping %s because it does not contain ' \
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
