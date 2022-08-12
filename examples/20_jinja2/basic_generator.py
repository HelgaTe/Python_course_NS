from jinja2 import Template

template = Template('''
hostname {{name}}
!
interface Loopback255
 description Management loopback
 ip address 10.255.{{id}}.1 255.255.255.255
!
interface GigabitEthernet0/0
 description LAN to {{name}} sw1 {{int}}
 ip address {{ip}} 255.255.255.0
!
router ospf 10
 router-id 10.255.{{id}}.1
 auto-cost reference-bandwidth 10000
 network 10.0.0.0 0.255.255.255 area 0
''')

data = [
    {'id': '11','name': 'Liverpool', 'int': 'Gi1/0/1','ip': '10.1.1.1'},
    {'id': '21', 'name': 'London', 'int': 'Gi1/0/2','ip': '10.2.2.1'},
    {'id': '31', 'name': 'Coventry', 'int': 'Gi1/0/3','ip': '10.3.3.1'},
]
# if one of the params is missing, jinja is ignoring this instance (by default) and doesn't raise an exception, but the output will be incorrect
# this allows us to decide how to handle exceptional case (e.g. if param is missing -> put default variable)
# if it is required to deal with such cases : set add param in Environment <undefined = jinja2.StrictUndefined>


for param in data:
    print(template.render(param))
    print('='*40)
'''
Examples: # configuration for single device <Liverpool>

$ python generator.py 

hostname Liverpool
!
interface Loopback255
 description Management loopback
 ip address 10.255.11.1 255.255.255.255
!
interface GigabitEthernet0/0
 description LAN to Liverpool sw1 Gi1/0/17
 ip address 10.1.1.10 255.255.255.0
!
router ospf 10
 router-id 10.255.11.1
 auto-cost reference-bandwidth 10000
 network 10.0.0.0 0.255.255.255 area 0
'''
