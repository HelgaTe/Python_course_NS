# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""
from tabulate import tabulate

def print_ip_table (ip_reachable_list, ip_unreachable_list):
    data = {
        'Reachable': ip_reachable_list,
        'Unreachable': ip_unreachable_list}
    output=tabulate(data,headers='keys')
    print(type(output))
    return output


reach_ip = ["10.10.1.7", "10.10.1.8", "10.10.1.9", "10.10.1.15"]
unreach_ip = ["10.10.2.1", "10.10.1.2"]

print(print_ip_table(reach_ip,unreach_ip))
