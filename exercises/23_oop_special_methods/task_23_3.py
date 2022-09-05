# -*- coding: utf-8 -*-

"""
Задание 23.3

Скопировать и изменить класс Topology из задания 22.1x.

Добавить метод, который позволит выполнять сложение двух экземпляров класса Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
"""

'''
ALERT :
Пименения метода update() для объеденения 2х словарей невозможно в данном случаи, потому что 
метод изменяет один из словарей. А наша задача, создать третий словарь без изменения исходных.
The problem is solved >>> dict3 = {** dict1, ** dict} 
'''

from pprint import pprint


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        self.topology = {}
        for key, value in topology_dict.items():
            if not self.topology.get(value) == key:
                self.topology[key] = value
        return self.topology

    def __add__(self, other):
        # return {**self.topology, **other.topology}
        return Topology({**self.topology, **other.topology})

    def delete_link(self, delt1, delt2):
        if self.topology.get(delt1) == delt2:
            del self.topology[delt1]
        elif self.topology.get(delt2) == delt1:
            del self.topology[delt2]
        else:
            print('Такого соединения нет')

    def delete_node(self, node):
        n_top = self.topology.copy()
        for key, value in n_top.items():
            if node in key or node in value:
                del self.topology[key]
            else:
                print("Такого устройства нет")

    def add_link(self, add1, add2):
        n_top = self.topology.copy()
        for i in n_top.items():
            if add1 in i and add2 in i:
                print('Такое соединение существует')
            elif add1 in i or add2 in i:
                print('Cоединение с одним из портов существует')
            else:
                new_link = {add1: add2}
                self.topology.update(new_link)


if __name__ == '__main__':
    topology_example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R3", "Eth0/1"): ("R4", "Eth0/0"),
        ("R3", "Eth0/2"): ("R5", "Eth0/0"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    }

    topology_example2 = {
        ("R1", "Eth0/4"): ("R7", "Eth0/0"),
        ("R1", "Eth0/6"): ("R9", "Eth0/0"),
    }

    top1 = Topology(topology_example)
    top2 = Topology(topology_example2)

    top3 = top1 + top2
    pprint(top3)

    # print('='*40)
    # print(top1)
    # print('=' * 40)
    # print(top2)
