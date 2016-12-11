import click
from tabulate import tabulate

from EasyEuler import data


TABLE_HEADERS = ('ID', 'Name', 'Difficulty')


@click.command()
@click.option('--sort', '-s', type=click.Choice(('id', 'difficulty')),
              default='id', help='Sort the list by problem attribute.')
def cli(sort):
    """ Lists all available problems. """

    problems = sorted(data.problems, key=lambda problem: problem[sort.lower()])
    problem_list = ((problem['id'], problem['name'],
                     '%d%%' % problem['difficulty']) for problem in problems)

    table = tabulate(problem_list, TABLE_HEADERS, tablefmt='fancy_grid')
    click.echo_via_pager(table)
