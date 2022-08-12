# -*- coding: utf-8 -*-
import yaml
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates')) # FileSystemLoader - путь к каталогу, где находятся шаблоны
template = env.get_template('router_template.txt')  # get template

with open('routers_info.yml') as f: # read file that contain data to fill in out the template
    routers = yaml.safe_load(f)

for router in routers:
    r1_conf = router['name'] + '_r1.txt' # create separate files for devices
    with open(r1_conf, 'w') as f:
        f.write(template.render(router))
