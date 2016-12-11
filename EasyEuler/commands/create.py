import os
import sys

import click

from EasyEuler import data
from EasyEuler.types import LanguageType, ProblemType
from EasyEuler.commands.generate_resources import generate_resources


@click.command()
@click.option('--path', '-p', type=click.Path(),
              help='Writes the file to PATH.')
@click.argument('problem', type=ProblemType())
@click.argument('language', type=LanguageType(),
                required=False, default=data.config['default language'])
def cli(problem, language, path):
    """
    Create the file for a problem.

    Simply specify a valid problem ID and the file will be created at
    euler_<id>.<extension> (if the PATH option isn't specified).

    Optionally, the LANGUAGE argument can be specified, which will then
    be used to identify an appropriate template for the file.

    """

    if path is None:
        filename_format = data.config['filename format']
        path = filename_format.format(id=problem['id'],
                                      extension=language['extension'])

    if os.path.exists(path) and not \
       click.confirm('%s already exists. Do you want to overwrite it?' %
                     click.format_filename(path)):
        return

    try:
        write_to_file(problem, language, path)
    except (FileNotFoundError, PermissionError) as exception:
        sys.exit('An exception occurred: %s' % exception)

    click.echo('Written to %s' % click.format_filename(path))

    if 'resources' in problem and \
        click.confirm('Generate resources for this problem?'):
            resource_path = click.prompt('Path (default: current directory)',
                                         default='.', show_default=False,
                                         type=click.Path(writable=True,
                                                         readable=False))
            generate_resources(problem['resources'], resource_path)


def write_to_file(problem, language, path):
    template_name = language.get('template', language['name'])
    template = data.templates.get_template(template_name)

    with open(path, 'w') as problem_file:
        problem_file.write(template.render(**problem))
