# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def get_int_vlan_map (config_filename):
    access_dict={}
    trunk_dict={}
    with open ('config_sw1.txt','r') as f:
        for line in f:
            line=line.rstrip()
            line_item=line.split()
            if 'FastEthernet' in line:
                intf=line_item[-1]
            elif 'access vlan' in line:
                vlan=int(line_item[-1])
                access_dict[intf]=vlan
            elif 'trunk allowed' in line:
                vlans=line_item[4::]
                vlans_int=[int(item) for item in vlans[0].split(',')]
                trunk_dict[intf]=vlans_int
    return access_dict, trunk_dict            
