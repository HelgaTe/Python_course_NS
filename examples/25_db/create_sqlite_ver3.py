import os
import re
import sqlite3

data_filename = 'dhcp_snooping.txt'
db_filename = 'dhcp_snooping4.db'
schema_filename = 'dhcp_snooping_schema.sql'

regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')

result = []

with open('dhcp_snooping.txt') as data:
    for line in data:
        match = regex.search(line)
        if match:
            result.append(match.groups())

db_exists = os.path.exists(db_filename)

conn = sqlite3.connect(db_filename)

if not db_exists: # проверка наличия файла БД, и файл dhcp_snooping.db будет создаваться только в том случае, если его нет
    print('Creating schema...')
    with open(schema_filename, 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    print('Done')
else:
    print('Database exists, assume dhcp table does, too.')

print('Inserting DHCP Snooping data')

for row in result:
    try:
        with conn:
            query = '''insert into dhcp (mac, ip, vlan, interface)
                       values (?, ?, ?, ?)'''
            conn.execute(query, row)
    except sqlite3.IntegrityError as e: # надо перехватывать исключение sqlite3.IntegrityError (относящееся к модулю), а не IntegrityError.
        print('Error occured: ', e)

conn.close()
