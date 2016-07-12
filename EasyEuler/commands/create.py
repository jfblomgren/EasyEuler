import sys
import os

import click

from EasyEuler import data
from EasyEuler.types import ProblemType, LanguageType


@click.command()
@click.option('--path', '-p', type=click.Path(),
              help='Writes the file to PATH.')
@click.option('--overwrite', '-o', is_flag=True,
              help='Overwrite the file if it already exists.')
@click.argument('problem', type=ProblemType())
@click.argument('language', type=LanguageType(),
                required=False, default='python')
def cli(problem, language, path, overwrite):
    """
    Create the file for a problem.

    Simply specify a valid problem ID and the file will be created at
    euler_<id>.<extension> (if the PATH option isn't specified).

    Optionally, the LANGUAGE argument can be specified, which will then be used
    to identify an appropriate template for the file.

    """

    if path is None:
        path = 'euler_%03d.%s' % (problem['id'], language['extension'])

    try:
        write_to_file(problem, language, path, overwrite)
    except (FileNotFoundError, PermissionError) as exception:
        sys.exit('An exception occurred: %s' % exception)
    except FileExistsError:
        sys.exit('%s already exists. Use the --overwrite flag to overwrite it' %
                 click.format_filename(path))

    click.echo('Written to %s' % click.format_filename(path))


def write_to_file(problem, language, path, overwrite):
    template = data.templates.get_template(language.get('template',
                                                        language['name']))

    if os.path.exists(path) and not overwrite:
        raise FileExistsError

    with open(path, 'w') as f:
        f.write(template.render(**problem))
