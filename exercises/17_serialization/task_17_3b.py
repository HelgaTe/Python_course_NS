# -*- coding: utf-8 -*-
"""
Задание 17.3b

Создать функцию transform_topology, которая преобразует топологию в формат подходящий
для функции draw_topology.

Функция ожидает как аргумент имя файла в формате YAML, в котором хранится топология.

Функция должна считать данные из YAML файла, преобразовать их соответственно,
чтобы функция возвращала словарь такого вида:
    {('R4', 'Fa 0/1'): ('R5', 'Fa 0/1'),
     ('R4', 'Fa 0/2'): ('R6', 'Fa 0/0')}

Функция transform_topology должна не только менять формат представления топологии,
но и удалять "дублирующиеся" соединения (их лучше всего видно на схеме, которую
генерирует функция draw_topology из файла draw_network_graph.py).
Тут "дублирующиеся" соединения, это ситуация когда в словаре есть два соединения:
    ("R1", "Eth0/0"): ("SW1", "Eth0/1")
    ("SW1", "Eth0/1"): ("R1", "Eth0/0")

Из-за того что один и тот же линк описывается дважды, на схеме будут лишние соединения.
Задача оставить только один из этих линков в итоговом словаре, не важно какой.

Проверить работу функции на файле topology.yaml (должен быть создан в задании 17.3a).
На основании полученного словаря надо сгенерировать изображение топологии
с помощью функции draw_topology.
Не копировать код функции draw_topology из файла draw_network_graph.py.

Результат должен выглядеть так же, как схема в файле task_17_3b_topology.svg

При этом:
* Интерфейсы должны быть записаны с пробелом Fa 0/0
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме
* На схеме не должно быть "дублирующихся" линков


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

"""
import yaml
from pprint import pprint

from draw_network_graph import draw_topology

def transform_topology (topology_file) :

    topology_upd_dict={}

    with open (topology_file) as f:
        topology_dict=yaml.safe_load(f)

        for key,value in topology_dict.items():
            main_dev=key
            for k,v in value.items():
                k_upd=(main_dev, k)
                for k0,v0 in v.items():
                    v_upd=(k0,v0)
                    topology_upd_dict[k_upd]=v_upd
    unique_topology_map={}
    for k_t_upd,v_t_upd in topology_upd_dict.items():
        k_t_upd,v_t_upd=sorted([k_t_upd,v_t_upd])
        unique_topology_map[k_t_upd]=v_t_upd

    return unique_topology_map
    # return topology_upd_dict


if __name__ == "__main__":
    result=transform_topology('topology.yaml')
    pprint(result)
    draw_topology(result,'topology_test_olga')