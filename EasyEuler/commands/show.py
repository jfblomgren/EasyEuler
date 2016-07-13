import click

from EasyEuler import data
from EasyEuler.types import ProblemType


@click.command()
@click.argument('problem', type=ProblemType())
def cli(problem):
    """ Show a problems description. """

    template = data.templates.get_template('description')
    description = template.render(**problem)
    click.echo(description)
