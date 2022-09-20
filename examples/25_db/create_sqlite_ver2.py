import re
import sqlite3

regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

result = []

with open('dhcp_snooping.txt') as data:
    for line in data:
        match = regex.search(line)
        if match:
            result.append(match.groups())

conn = sqlite3.connect('dhcp_snooping4.db') # create db (open if exits)

# print('Creating schema...')
# with open('dhcp_snooping_schema.sql', 'r') as f: # create table based on template (writen into file)
#     schema = f.read()
#     conn.executescript(schema) # executescript >>> выполнять команды SQL, которые прописаны в файле
# print('Done')

print('Inserting DHCP Snooping data')

for row in result:
    try:
        with conn:
            query = '''insert into dhcp (mac, ip, vlan, interface)
                       values (?, ?, ?, ?)'''
            conn.execute(query, row)
    except sqlite3.IntegrityError as e:
        print('Error occured: ', e)

conn.close()
