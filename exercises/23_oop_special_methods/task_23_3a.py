# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""

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

    def __iter__(self):
        return iter(self.topology.items())



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

    top1 = Topology(topology_example)
    for link in top1:
        print(link)
