import json
from pprint import pprint

with open('sw_templates.json') as f:
    templates = json.load(f)

pprint(templates)

for section, commands in templates.items():
    print(section)
    print('\n'.join(commands))
