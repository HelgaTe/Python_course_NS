# -*- coding: utf-8 -*-
import sqlite3
'''
Использование модуля sqlite3 без явного создания курсора
'''
data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]


con = sqlite3.connect('dhcp_snooping2.db')

# execute - метод для выполнения одного выражения SQL
con.execute('''create table switch
            (mac text not NULL primary key, hostname text, model text, location text)'''
            )

query = 'INSERT into switch values (?, ?, ?, ?)'
# executemany - метод позволяет выполнить одно выражение SQL для последовательности параметров
con.executemany(query, data)
con.commit()

for row in con.execute('select * from switch'):
    print(row)

con.close()

# stdout:
"""
('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str')
('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str')
('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str')
('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')
"""

