import re
from pprint import pprint

# regex=r'Host (\S+) .+ port (\S+) and port (\S+)'
#
# ports=set() # чтобы убрать порты, которые дублируются
# with open ('log.txt') as f:
#     for line in f:
#         m=re.search(regex,line)
#         if m: # чтобы перехватить ошибку None - в отношении строк файла, где не содержитться полезных строк
#             print(m.groups())
#             print(m.group(2,3))
#             ports.update(m.group(2,3))
#
# # print(ports)


# mail_log = ['Jun 18 14:10:35 client-ip=154.10.180.10 from=user1@gmail.com, size=551',
#             'Jun 18 14:11:05 client-ip=150.10.180.10 from=user2.test@gmail.com, size=768']
#
# for message in mail_log:
#     match = re.search(r'\w+\.?\w+@\w+\.\w+', message)
#     if match:
#         print("Found email: ", match.group())




# def parse_shooting (outcome):
#     regex=r'(?P<mac>\S+) \s+ (?P<ip>(\d+\.){3}\d+) .+ (?P<vlan>\d+)'
#
#     result=[]
#
#     for line in outcome.split('\n'):
#         match=re.search(regex,line)
#         if match:
#             result.append(match.groupdict())
#     return result
#
# if __name__=="__main__":
#     with open('dhcp_snooping.txt') as f:
#         content=f.read()
#     pprint(parse_shooting(content))


# def parse_shooting (outcome):
#     regex=r'(?P<ip>(\d+\.){3}\d+) .+ (?P<vlan>\d+)'
#
#     result_dict={}
#
#     for line in outcome.split('\n'):
#         match=re.search(regex,line)
#         if match:
#             ip=match.group(1)
#             vlan=match.group(2)
#             result_dict[ip]=vlan
#     return result_dict
#
# if __name__=="__main__":
#     with open('dhcp_snooping.txt') as f:
#         content=f.read()
#     pprint(parse_shooting(content))

# with open ('CAM_table.txt') as f:
#     content=f.read()
#     m=re.findall('(\d+) +(\S+) +\S+ +(\S+)',content)
#     pprint(m)


mac_table = '''
100    aabb.cc10.7000    DYNAMIC     Gi0/1
200    aabb.cc20.7000    DYNAMIC     Gi0/2
300    aabb.cc30.7000    DYNAMIC     Gi0/3
100    aabb.cc40.7000    DYNAMIC     Gi0/4
500    aabb.cc50.7000    DYNAMIC     Gi0/5
200    aabb.cc60.7000    DYNAMIC     Gi0/6
300    aabb.cc70.7000    DYNAMIC     Gi0/7
'''

print(re.sub(r' *(\d+) +'
             r'([a-f0-9]+)\.'
             r'([a-f0-9]+)\.'
             r'([a-f0-9]+) +\w+ +'
             r'(\S+)',
             r'vlan \1 \2:\3:\4 \5',
             mac_table))

print(re.sub(r' *(\d+) +'
             r'([a-f0-9]+)\.'
             r'([a-f0-9]+)\.'
             r'([a-f0-9]+) +\w+ +'
             r'(\S+)',
             r'VLAN : \1 mac adr : \2:\3:\4 intf :\5',
             mac_table))
