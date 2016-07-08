import os

import click


COMMAND_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              'commands'))


class CommandLineInterface(click.MultiCommand):
    def list_commands(self, ctx):
        commands = []

        for filename in os.listdir(COMMAND_FOLDER):
            if filename.endswith('.py') and filename != '__init__.py':
                commands.append(filename[:-3].replace('_', '-'))

        commands.sort()
        return commands

    def get_command(self, ctx, name):
        # We don't want foo_bar to be interpreted as a valid command,
        # but we still want foo-bar to be.
        name = name.replace('_', '').replace('-', '_')

        try:
            command = __import__('EasyEuler.commands.%s' % name,
                                 None, None, ['cli'])
        except ImportError:
            return
        return command.cli


cli = CommandLineInterface()
