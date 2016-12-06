import os


BASE = os.path.abspath(os.path.dirname(__file__))
DATA = os.path.join(BASE, 'data')

COMMANDS = os.path.join(BASE, 'commands')
RESOURCES = os.path.join(DATA, 'resources')
PROBLEMS = os.path.join(DATA, 'problems.json')

CONFIGS = [os.path.join(BASE, 'config.json')]
TEMPLATES = [os.path.join(BASE, 'templates')]

HOME = os.environ.get('HOME')
if HOME is not None:
    DEFAULT_XDG_CONFIG_HOME = os.path.join(HOME, '.config')
    XDG_CONFIG_HOME = os.environ.get('XDG_CONFIG_HOME', DEFAULT_XDG_CONFIG_HOME)
    XDG_CONFIG_DIRS = os.environ.get('XDG_CONFIG_DIRS', '/etc/xdg').split(':')
    CONFIG_DIRS = list(reversed(XDG_CONFIG_DIRS)) + [XDG_CONFIG_HOME]

    for config_dir in CONFIG_DIRS:
        if os.path.isabs(config_dir):
            config_path = os.path.join(config_dir, 'EasyEuler/config.json')
            template_path = os.path.join(config_dir, 'EasyEuler/templates')
            CONFIGS.append(config_path)
            TEMPLATES.append(template_path)
