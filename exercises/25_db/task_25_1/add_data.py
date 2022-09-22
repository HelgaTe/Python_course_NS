import glob
import os
import re
import sqlite3

import yaml

'''
add_data_status.py - с помощью этого скрипта, выполняется добавление данных в БД.
Скрипт должен добавлять данные из вывода sh ip dhcp snooping binding
и информацию о коммутаторах

Соответственно, в файле add_data_status.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно
   также заполнять. Имя коммутатора определяется по имени файла с данными

Пример выполнения скрипта, когда база данных еще не создана:
$ python add_data_status.py
База данных не существует. Перед добавлением данных, ее надо создать

Пример выполнения скрипта первый раз, после создания базы данных:
$ python add_data_status.py
Добавляю данные в таблицу switches...
Добавляю данные в таблицу dhcp...

Пример выполнения скрипта, после того как данные были добавлены в таблицу
(порядок добавления данных может быть произвольным, но сообщения должны
выводиться аналогично выводу ниже):

$ python add_data_status.py
Добавляю данные в таблицу switches...
При добавлении данных: ('sw1', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw2', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw3', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
Добавляю данные в таблицу dhcp...
При добавлении данных: ('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:07:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:BC:3F:A6:50', '100.1.1.6', '3', 'FastEthernet0/20', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:22:11:A6:50', '100.1.1.7', '3', 'FastEthernet0/21', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BB:3D:D6:58', '10.1.10.20', '10', 'FastEthernet0/7', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:B4:A3:3E:5B:69', '10.1.5.20', '5', 'FastEthernet0/5', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:C5:B3:7E:9B:60', '10.1.5.40', '5', 'FastEthernet0/9', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BC:3F:A6:50', '10.1.10.60', '20', 'FastEthernet0/2', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
'''

def parse_dhcp_snoop(filename):
    regex = re.compile("(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)") # regex for <sw*_dhcp_snooping> file content
    sw = re.search("(\w+)_dhcp_snooping.txt", filename).group(1) # получить sw_num
    with open(filename) as f:
        result = [match.groups() + (sw,) for match in regex.finditer(f.read())] # получить данные в виде кортежа
    return result


def add_data(db, query, data): # общая функция для записи данных в БД
    connection = sqlite3.connect(db) # подключиться/открыть колнкретную БД
    for row in data:
        try:
            with connection:
                connection.execute(query, row) # метод для выполнения одного выражения sqlite3 (create, insert)
        except sqlite3.IntegrityError as err:
            print("При добавлении данных:", row, "Возникла ошибка:", err)
    connection.close()


def add_sw_data(db_name, sw_data_file): # записать данные о коммутаторах, находятся в файле switches.yml
    db_exists = os.path.exists(db_name)
    if not db_exists: # проверить существует ли БД
        print("База данных не существует. Перед добавлением данных, ее надо создать")
        return
    print("Добавляю данные в таблицу switches...")
    query_switches = "insert into switches values (?,?)" # запрос для записи данных
    with open(sw_data_file) as f:
        switches = yaml.safe_load(f) # считать файл - данные в виде сложенного словаря
    sw_data = list(switches["switches"].items()) # получить данные в виде кортежа
    add_data(db_name, query_switches, sw_data) # записать данные из файла в БД


def add_dhcp_data(db_name, data_files):
    db_exists = os.path.exists(db_name)
    if not db_exists: # проверить существует ли БД
        print("База данных не существует. Перед добавлением данных, ее надо создать")
        return
    print("Добавляю данные в таблицу dhcp...")
    query = "insert into dhcp values (?, ?, ?, ?, ?)" # запрос для записи данных
    result = []
    for filename in data_files:
        result.extend(parse_dhcp_snoop(filename))
    add_data(db_name, query, result)


if __name__ == "__main__":
    db_filename = "dhcp_snooping.db"
    dhcp_snoop_files = glob.glob("sw*_dhcp_snooping.txt")
    add_sw_data(db_filename, "switches.yml")
    add_dhcp_data(db_filename, dhcp_snoop_files)