import glob
from pprint import pprint
import os
import re
import sqlite3
import yaml

"""
upon bd created, add last_active column by the following command into terminal:
    dhcp_snooping.db> alter table dhcp add column 'last_active' 'datetime'
and then you can add data into db by running add_data_status.py 
"""

def add_data(connection, query, data):  # общая функция для записи данных в БД
    # connection - переменная, которая создается в нижестоящих функциях (add_dhcp_data & add_sw_data)
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as err:
            print("При добавлении данных:", row, "Возникла ошибка:", err)


def parse_dhcp_snoop(filename): # с помощью regex отобрать информацию для записи в бд
    regex = re.compile("(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)")  # regex for <sw*_dhcp_snooping> file content
    sw = re.search("(\w+)_dhcp_snooping.txt", filename).group(1)  # получить номер switch из названия файла
    with open(filename) as f:
        result = [match.groups() + (sw,) for match in regex.finditer(f.read())]  # прочитать содержимое файла и получить данные в виде кортежа
    return result


def add_dhcp_data(db_name, data_files):
    connection = sqlite3.connect(db_name)  # подклчиться к конкретной бд
    connection.execute("update dhcp set active = 0")  # отметить замененые данные,как неактивные
    query = "replace into dhcp values (?, ?, ?, ?, ?, ?, datetime('now'))"  # добавление/замена (нарушение условия уникальности поля) данных в табл
    # при добавлении записи, для которой не возникает нарушения уникальности поля, REPLACE работает как обычный INSERT
    for filename in data_files:
        result = parse_dhcp_snoop(filename)
        updated_result = (row + (1,) for row in result)  # <row + (1,)> добавить стоблец с значением (1)
        add_data(connection, query, updated_result)
    connection.close()


def add_sw_data(db_name, sw_data_file):  # записать данные о коммутаторах, находятся в файле switches.yml
    connection = sqlite3.connect(db_name)
    query_switches = "insert into switches values (?,?)"  # запрос для записи данных
    with open(sw_data_file) as f:
        switches = yaml.safe_load(f)  # считать файл - данные в виде сложенного словаря
    sw_data = list(switches["switches"].items())  # получить данные в виде кортежа
    add_data(connection, query_switches, sw_data)  # записать данные из файла в БД
    connection.close()


if __name__ == "__main__":
    db_filename = "dhcp_snooping.db"
    sw_data = glob.glob('sw*_dhcp_snooping.txt')
    sw_new_data = glob.glob('new_data/sw*_dhcp_snooping.txt')

    add_dhcp_data(db_filename, sw_data)
    add_dhcp_data(db_filename, sw_new_data)
    add_sw_data(db_filename, "switches.yml")

# проверка того, что данные с файлов в формате sw_new_data считывается
# for i in sw_new_data:
#     print(i)
#     with open (i) as f:
#         print(f.read())
# for i in sw_data:
#     pprint(parse_dhcp_snoop(i))
