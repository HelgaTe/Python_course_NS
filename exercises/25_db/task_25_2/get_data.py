# -*- coding: utf-8 -*-
"""
Задание 25.2
"""
import sqlite3
from tabulate import tabulate


def get_dhcp_data(db_filename, table):  # вывести всё содержимое таблицы
    print(f'В таблице {table} такие записи: ')
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    output_tab = []
    for row in cursor.execute(f'select * from {table}'):
        output_tab.append(row)
    print(tabulate(output_tab))
    connection.close()


def get_data_by_key(db_filename, table, key, value):  # вывести инфо из таблицы, которая соответствует полю и значению
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()
    cursor.execute(f'select * from {table}')
    keys = []
    for row in cursor.description:  # собрать доступные имена столбцов таблицы
        keys.append(row[0])
    if key not in keys:
        print("Данный параметр не поддерживается.")
        print(f"Допустимые значения параметров: {keys}")
    query = f'select * from {table} WHERE {key} = ?'
    output_tab = []
    output_tab.append(keys)
    for row in connection.execute(query, (value,)):
        output_tab.append(row)
    print(f'Информация об устройствах с такими параметрами: {key} {value}')
    print(tabulate(output_tab))


def parse_db(db_filename, table, *args):
    if len(args) == 0:
        get_dhcp_data(db_filename, table)
    elif len(args) == 2:
        key, value = args
        get_data_by_key(db_filename, table, key, value)
    else:
        print('Пожалуйста, введите два или ноль аргументов')


if __name__ == '__main__':
    db_name = 'dhcp_snooping_25_1.db'
    tab = 'dhcp'

    # глобальная функция, которая автоматически определяет какую функцию применить:
    parse_db(db_name, tab)
    parse_db(db_name, tab, 'vlan', '3')

    # локальная функция, которую определили пользователь
    get_dhcp_data(db_name, tab) # вывести инфо из таблицы
    get_data_by_key(db_name, tab, key='vlan', value='10') # вывести инфо из таблицы, которая соответствует полю и значению
    get_data_by_key(db_name, tab, key='vl', value='10') # данного поля в табл не существует




