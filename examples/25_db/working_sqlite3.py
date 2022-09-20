import sqlite3

conn = sqlite3.connect('dhcp_snooping.db')  # объект <connection> - это подключение к конкретной БД
cursor = conn.cursor()  # после создания соединения надо создать объект <cursor> - основной способ работы с БД

'''
Метод execute
'''
# 1st step : создание таблицы switch с помощью метода execute
cursor.execute('create table switch (mac text not NULL primary key, hostname text, model text, location text)')
# now >> can write <sqlite3 dhcp_snooping.db '.shcema'> into terminal to see table structure

data = [
    ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
    ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
    ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
    ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]  # данные для записи в таблицу

query = "INSERT into switch values (?, ?, ?, ?)" # запрос

for row in data:  # передача данныех для записи
    cursor.execute(query,row) # второй аргумент, который передается методу execute, должен быть кортежем
conn.commit() # чтобы изменения были применены, нужно выполнить commit
# now >> can write <sqlite3 dhcp_snooping.db 'select * from switch'> into terminal to see table content

'''
Метод executemany
'''
data2 = [
    ('0000.1111.0001', 'sw5', 'Cisco 3750', 'London, Green Str'),
    ('0000.1111.0002', 'sw6', 'Cisco 3750', 'London, Green Str'),
    ('0000.1111.0003', 'sw7', 'Cisco 3750', 'London, Green Str'),
    ('0000.1111.0004', 'sw8', 'Cisco 3750', 'London, Green Str')] # данные для записи в таблицу

query = "INSERT into switch values (?, ?, ?, ?)" # запрос

cursor.executemany(query, data2)
conn.commit()
# <dhcp_snooping.db> select * from switch;> >> receive switch table, that includes data & data2

'''
Метод executescript
'''
cursor.executescript('''
    create table switch2 (
    hostname text not NULL primary key,
    location text
    );

    create table dhcp (
    mac text not NULL primary key,
    ip text,
    vlan text,
    interface text,
    switch text not null references switches(hostname)
    );
    ''')
# <dhcp_snooping.db> .tables> >>> current db includes 3 tables (dhcp, switch, switch2)


# # how to get info
cursor.execute('select * from dhcp')
cursor.fetchall()

