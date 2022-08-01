import pexpect
from pprint import pprint

r1=pexpect.spawn('ssh cisco@172.16.100.129')

r1.expect('Password')
r1.sendline('cisco')

# r1.expect('>')
# r1.sendline('terminal length 0')

r1.expect('>')
# r1.sendline('show version')
# r1.sendline('show cdp neighbors')
r1.sendline('sh ip interface brief')

r1.expect('>')
x=r1.before.decode('utf-8').splitlines()
r1.sendline('exit')

# print(x)

with open ('working_output.txt','w') as f:
    for line in x:
        f.writelines(line + '\n')


# import yaml
# from pprint import pprint
#
# with open("devices.yaml") as f:
#     devices = yaml.safe_load(f)
#     pprint(devices)

