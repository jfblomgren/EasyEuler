import sys

import click

from .utils import write_to_file, get_problem


@click.group()
def commands():
    pass


@click.command()
@click.option('--path', '-p', type=click.Path())
@click.option('--overwrite', '-o', is_flag=True)
@click.argument('problem_id', type=click.IntRange(1, None))
@click.argument('language', required=False, default='python')
def generate(problem_id, language, path, overwrite):
    problem = get_problem(problem_id)

    if problem is None:
        sys.exit('Problem %d does not exist' % problem_id)

    try:
        path, success = write_to_file(problem, language, path, overwrite)
    except (FileNotFoundError, PermissionError) as e:
        sys.exit('An exception occurred: %s' % e)

    if not success:
        sys.exit('%s already exists. Use the --overwrite flag to overwrite it' %
                 click.format_filename(path))

    click.echo('Written to %s' % click.format_filename(path))

commands.add_command(generate)
