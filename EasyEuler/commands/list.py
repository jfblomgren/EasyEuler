import click

from EasyEuler import data


@click.command()
@click.option('--long', '-l', is_flag=True,
              help='Include problem descriptions.')
@click.option('--sort', '-s', type=click.Choice(['id', 'difficulty']),
              default='id', help='Sort the list by problem attribute.')
def cli(long, sort):
    """ Lists all available problems. """

    problem_list = []
    for problem in sorted(data.problems, key=lambda p: p[sort.lower()]):
        problem_string = 'Problem {id}: {name}'.format(**problem)

        if long:
            problem_string += '\n=========================================\n\n'
            problem_string += problem['description']
            problem_string += '\n\n========================================='

        problem_list.append(problem_string)
    click.echo_via_pager('\n'.join(problem_list))
