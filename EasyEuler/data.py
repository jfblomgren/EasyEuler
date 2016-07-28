import collections
import json
import os

from jinja2 import Environment, FileSystemLoader

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')
TEMPLATE_PATH = os.path.join(BASE_PATH, 'templates')
CONFIG_PATH = os.path.join(BASE_PATH, 'config.json')

with open('%s/problems.json' % DATA_PATH) as f:
    problems = json.load(f)


class ConfigurationDictionary(collections.MutableMapping):
    def __init__(self, config_paths):
        self.config = {}

        for config_path in config_paths:
            if os.path.exists(config_path):
                with open(config_path) as f:
                    self.config = self.update(self.config, json.load(f))

    def update(self, config, updates):
        for key, value in updates.items():
            if isinstance(value, collections.Mapping):
                updated = self.update(config.get(key, {}), value)
                config[key] = updated
            else:
                config[key] = value
        return config

    def __getitem__(self, key):
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]

    def __iter__(self):
        return iter(self.config)

    def __len__(self):
        return len(self.config)


home = os.environ.get('HOME')
if home is None:
    config_paths = []
    template_paths = []
else:
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME',
                                     os.path.join(home, '.config'))
    xdg_config_dirs = os.environ.get('XDG_CONFIG_DIRS', '/etc/xdg')
    config_dirs =  [xdg_config_home] + xdg_config_dirs.split(':')
    config_paths = [os.path.join(config_dir, 'EasyEuler/config.json')
                    for config_dir in config_dirs if os.path.isabs(config_dir)]
    template_paths = [os.path.join(config_dir, 'EasyEuler/templates')
                      for config_dir in config_dirs if os.path.isabs(config_dir)]
config_paths.append(CONFIG_PATH)
template_paths.append(TEMPLATE_PATH)

config = ConfigurationDictionary(reversed(config_paths))
templates = Environment(loader=FileSystemLoader(reversed(template_paths)))
