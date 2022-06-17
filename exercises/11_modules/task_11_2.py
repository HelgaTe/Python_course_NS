# -*- coding: utf-8 -*-
"""
Задание 11.2

Создать функцию create_network_map, которая обрабатывает
вывод команды show cdp neighbors из нескольких файлов и объединяет его в одну
общую топологию.

У функции должен быть один параметр filenames, который ожидает как аргумент
список с именами файлов, в которых находится вывод команды show cdp neighbors.

Функция должна возвращать словарь, который описывает соединения между
устройствами. Структура словаря такая же, как в задании 11.1:
    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}


Cгенерировать топологию, которая соответствует выводу из файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt

Не копировать код функций parse_cdp_neighbors и draw_topology.
Если функция parse_cdp_neighbors не может обработать вывод одного из файлов
с выводом команды, надо исправить код функции в задании 11.1.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
infiles = [
    "sh_cdp_n_sw1.txt",
    "sh_cdp_n_r1.txt",
    "sh_cdp_n_r2.txt",
    "sh_cdp_n_r3.txt",
]

from task_11_1 import parse_cdp_neighbors


def create_network_map(filenames):
    final = []
    for file in infiles:
        with open(file) as f:
            command_output = f.read()
            result = parse_cdp_neighbors(command_output)
            final.append(result)
            keys = []
            values = []
            for item in final:
                key = list(item.keys())
                value = list(item.values())
                keys.append(key)
                values.append(value)
                keys_list = [item for keys_list in keys for item in keys_list]
                values_list = [item for values_list in values for item in values_list]
                fin_dict = dict(zip(keys_list, values_list))
    return fin_dict


network_map_result = create_network_map(infiles)
print(network_map_result)
