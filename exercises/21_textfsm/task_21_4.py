# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

from netmiko import ConnectHandler
from textfsm import clitable
import yaml
from pprint import pprint


def send_and_parse_show_command(device_dict, command, templates_path, index='index'):
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    comm_output = ssh.send_command(command)

    attributes = {'Command': command, 'Vendor': 'cisco_ios'}
    cli_table = clitable.CliTable(index, templates_path)
    cli_table.ParseCmd(comm_output, attributes)
    k=cli_table.header
    parsed_dict=[dict(zip(k,v)) for v in cli_table]
    return parsed_dict


if __name__ == "__main__":
    command = 'sh ip int br'

    with open ('devices.yaml') as f:
        dev_dict=yaml.safe_load(f)
        # pprint(dev_dict) # all devices are loaded, but the func is expecting the only one device
    pprint(send_and_parse_show_command(dev_dict[0],command,'templates'))