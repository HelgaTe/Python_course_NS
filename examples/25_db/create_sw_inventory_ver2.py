# -*- coding: utf-8 -*-
import sqlite3

data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

con = sqlite3.connect('dhcp_snooping3.db')  # create (or open if exists) database
con.execute('''create table switch
               (mac text not NULL primary key, hostname text, model text, location text)'''
            )  # create table within db, tab structure is described

try:
    with con:
        query = 'INSERT into switch values (?, ?, ?, ?)'  # insert data into table
        con.executemany(query, data)

except sqlite3.IntegrityError as e:
    print('Error occured: ', e)

for row in con.execute('select * from switch'):
    print(row)

con.close()

# stdout:
'''
('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')
('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')
('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')
'''
