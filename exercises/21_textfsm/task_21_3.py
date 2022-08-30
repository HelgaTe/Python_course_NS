# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""
from textfsm import clitable
from pprint import pprint


def parse_command_dynamic(command_output, attributes_dict, index_file='index', templ_path='templates'):
    cli_table = clitable.CliTable(index_file,
                                  templ_path)  # инициализировать класс, передав ему имя файла, в котором хранится соответствие между шаблонами и командами, и указать имя каталога, в котором хранятся шаблоны
    cli_table.ParseCmd(command_output, attributes_dict)
    k = cli_table.header
    result = [dict(zip(k, v)) for v in cli_table]
    return result


if __name__ == '__main__':
    attr_dict = {'Command': 'sh ip int br', 'Vendor': 'cisco_ios'}
    with open('output/sh_ip_int_br.txt') as f:
        comm_output = f.read()  # считать вывод команды из файла

        pprint(parse_command_dynamic(comm_output, attr_dict))
