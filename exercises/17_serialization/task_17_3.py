# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re


def parse_sh_cdp_neighbors(command_output):
    """
    функция обрабатывает вывод команды show cdp neighbors
    @param command_output: вывод команды одной строкой (не имя файла)
    @return: словарь, который описывает соединения между устройствами
    """
    regex = re.compile(
        r'(?P<dev_id>\S+) +'
        r'(?P<loc_intf>\S+ \d+\/\d+) .+'
        r'(?P<port>Eth \S+)'
    )

    config_dict={}
    main_dev=re.search(r'(?P<main_dev>\S+)>',command_output).group('main_dev')
    config_dict[main_dev]={}

    for match in regex.finditer(command_output):
        dev_id,loc_intf,port=match.groups()
        config_dict[main_dev][loc_intf]={dev_id:port}

    return config_dict




if __name__ == "__main__":
    with open ('sh_cdp_n_r1.txt') as f:
        print(parse_sh_cdp_neighbors(f.read()))

# regex=re.compile(
#         r'(?P<dev_id>\S+) +'
#         r'(?P<loc_intf>\S+ \d+\/\d+) .+'
#         r'(?P<port>Eth \S+)'
#     )

# config_dict = {}
# with open('sh_cdp_n_r1.txt') as f:
#     main_dev = re.search(r'(?P<main_dev>\S+)>', f.read()).group('main_dev')
#     config_dict[main_dev] = {}
#
# with open('sh_cdp_n_r2.txt') as f:
#     for match in regex.finditer(f.read()):
#         dev_id, loc_intf, port = match.groups()
#         config_dict[main_dev][loc_intf] = {dev_id: port}
#         print(config_dict)
#


