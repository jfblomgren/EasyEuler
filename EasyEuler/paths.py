import os


BASE = os.path.abspath(os.path.dirname(__file__))

# Folders
TEMPLATES = os.path.join(BASE, 'templates')
COMMANDS = os.path.join(BASE, 'commands')
DATA = os.path.join(BASE, 'data')
RESOURCES = os.path.join(DATA, 'resources')

# Files
CONFIG = os.path.join(BASE, 'config.json')
PROBLEMS = os.path.join(DATA, 'problems.json')
