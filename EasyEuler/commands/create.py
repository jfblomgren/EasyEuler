import os
import sys

import click

from EasyEuler import data
from EasyEuler.types import LanguageType, ProblemType


@click.command()
@click.option('--path', '-p', type=click.Path(),
              help='Writes the file to PATH.')
@click.argument('problem', type=ProblemType())
@click.argument('language', type=LanguageType(),
                required=False, default='python')
def cli(problem, language, path):
    """
    Create the file for a problem.

    Simply specify a valid problem ID and the file will be created at
    euler_<id>.<extension> (if the PATH option isn't specified).

    Optionally, the LANGUAGE argument can be specified, which will then
    be used to identify an appropriate template for the file.

    """

    if path is None:
        path = 'euler_%03d.%s' % (problem['id'], language['extension'])

    if os.path.exists(path) and not click.confirm('%s already exists. Do you '
                                                  'want to overwrite it?' % path):
        return

    try:
        write_to_file(problem, language, path)
    except (FileNotFoundError, PermissionError) as exception:
        sys.exit('An exception occurred: %s' % exception)

    click.echo('Written to %s' % click.format_filename(path))


def write_to_file(problem, language, path):
    template = data.templates.get_template(language.get('template',
                                                        language['name']))

    with open(path, 'w') as f:
        f.write(template.render(**problem))
