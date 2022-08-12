# -*- coding: utf-8 -*-

# <<< Initial example >>>

# import yaml
# from router_template import template_r1
#
# with open('routers_info.yml') as f:
#     routers = yaml.safe_load(f)
#
# for router in routers:
#     r1_conf = router['name'] + '_r1.txt'
#     with open(r1_conf, 'w') as f:
#         f.write(template_r1.render(router))


# <<< Full import >>>
from jinja2 import Environment,FileSystemLoader
import yaml
from pprint import pprint

env=Environment(loader=FileSystemLoader('.'))
templ=env.get_template('router_template.py')

with open ('routers_info.yml') as f:
    routers=yaml.safe_load(f)
    # pprint(routers)

for r in routers:
    r1_conf=r['name'] + '_ver2.txt'
    with open (r1_conf,'w') as dest:
        dest.write(templ.render(r))