import collections
import json
import os

from jinja2 import Environment, FileSystemLoader

from EasyEuler import paths


class ProblemList(collections.Sequence):
    def __init__(self, problems):
        self._problems = problems

    def get(self, problem_id):
        if problem_id < 1 or len(self) < problem_id:
            # We don't want a negative index,
            # because it'll wrap back around.
            return None
        return self[problem_id]

    def __getitem__(self, problem_id):
        return self._problems[problem_id - 1]

    def __len__(self):
        return len(self._problems)


class ConfigurationDictionary(collections.Mapping):
    def __init__(self, configs):
        self._config = {}

        for config in configs:
            self._config = self._update(self._config, config)

    def _update(self, config, updates):
        for key, value in updates.items():
            if isinstance(value, collections.Mapping):
                updated = self._update(config.get(key, {}), value)
                config[key] = updated
            else:
                config[key] = value
        return config

    def get_language(self, key, value):
        for name, options in self._config['languages'].items():
            if options[key] == value:
                return {'name': name, **options}
        return None

    def __getitem__(self, key):
        return self._config[key]

    def __iter__(self):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError


CONFIG_LIST = []
for CONFIG_PATH in paths.CONFIGS:
    if not os.path.exists(CONFIG_PATH):
        continue

    with open(CONFIG_PATH) as conf:
        CONFIG_LIST.append(json.load(conf))

with open(paths.PROBLEMS) as f:
    PROBLEM_LIST = json.load(f)

config = ConfigurationDictionary(CONFIG_LIST)
problems = ProblemList(PROBLEM_LIST)
templates = Environment(loader=FileSystemLoader(paths.TEMPLATES))
