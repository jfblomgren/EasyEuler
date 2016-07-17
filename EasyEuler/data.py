import json
import os

from jinja2 import Environment, FileSystemLoader


BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')
TEMPLATE_PATH = os.path.join(BASE_PATH, 'templates')
CONFIG_PATH = os.path.join(BASE_PATH, 'config.json')

templates = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

with open(CONFIG_PATH) as f:
    config = json.load(f)

with open('%s/problems.json' % DATA_PATH) as f:
    problems = json.load(f)
