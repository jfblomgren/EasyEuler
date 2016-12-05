import collections
import json
import os

from jinja2 import Environment, FileSystemLoader

from EasyEuler import paths


class ProblemStore(collections.Sequence):
    def __init__(self):
        with open(paths.PROBLEMS) as f:
            self.problems = json.load(f)

    def get(self, id):
        if id < 1 or len(self.problems) < id:
            # We don't want a negative index, because it'll wrap back around.
            return None
        return self.problems[id - 1]

    def __getitem__(self, id):
        return self.problems[id - 1]

    def __len__(self):
        return len(self.problems)


class ConfigurationDictionary(collections.Mapping):
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

    def get_language(self, key, value):
        for name, options in self.config['languages'].items():
            if options[key] == value:
                return {'name': name, **options}
        return None

    def __getitem__(self, key):
        return self.config[key]

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
    config_dirs = [xdg_config_home] + xdg_config_dirs.split(':')
    config_paths = [os.path.join(config_dir, 'EasyEuler/config.json')
                    for config_dir in config_dirs if os.path.isabs(config_dir)]
    template_paths = [os.path.join(config_dir, 'EasyEuler/templates')
                      for config_dir in config_dirs if os.path.isabs(config_dir)]
config_paths.append(paths.CONFIG)
template_paths.append(paths.TEMPLATES)

config = ConfigurationDictionary(reversed(config_paths))
problems = ProblemStore()
templates = Environment(loader=FileSystemLoader(reversed(template_paths)))
