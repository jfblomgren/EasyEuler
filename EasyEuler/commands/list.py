import click
from tabulate import tabulate

from EasyEuler import data


@click.command()
@click.option('--sort', '-s', type=click.Choice(['id', 'difficulty']),
              default='id', help='Sort the list by problem attribute.')
def cli(sort):
    """ Lists all available problems. """

    problems = sorted(data.problems, key=lambda p: p[sort.lower()])
    problem_list = [(problem['id'], problem['name'], problem['difficulty'])
                    for problem in problems]

    problem_table = tabulate(problem_list, ['ID', 'Name', 'Difficulty'],
                             tablefmt='fancy_grid')
    click.echo_via_pager(problem_table)
