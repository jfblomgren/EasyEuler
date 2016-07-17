import click

from EasyEuler import data


@click.command()
@click.option('--sort', '-s', type=click.Choice(['id', 'difficulty']),
              default='id', help='Sort the list by problem attribute.')
def cli(sort):
    """ Lists all available problems. """

    problem_list = []
    for problem in sorted(data.problems, key=lambda p: p[sort.lower()]):
        problem_list.append('Problem {id}: {name}'.format(**problem))
    click.echo_via_pager('\n'.join(problem_list))
