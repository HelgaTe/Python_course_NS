# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

"""
import glob
import yaml
from task_17_3 import parse_sh_cdp_neighbors

def generate_topology_from_cdp (list_of_files,save_to_filename=None):
    """
    функция обрабатывает вывод команды show cdp neighbor из нескольких файлов
    и записывает итоговую топологию в один словарь
    @param list_of_files: список файлов из которых надо считать вывод команды sh cdp neighbor
    @param save_to_filename: имя файла в формате YAML, в который сохранится топология
             * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
             * топология сохраняется только, если save_to_filename как аргумент указано имя файла
             # эти условия реализованы через условие  if save_to_filename:
    """
    topology_dic={}
    for file in list_of_files:
        with open (file) as input_f:
            parse_result=parse_sh_cdp_neighbors(input_f.read())
            for key,value in parse_result.items():
                topology_dic[key]=value
    if save_to_filename: # значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
        with open (save_to_filename,'w') as final_f:
            yaml.dump(topology_dic,final_f)

    return topology_dic



if __name__ == "__main__":
    sh_cdp_n_files = glob.glob("sh_cdp_n*.txt")
    generate_topology_from_cdp(sh_cdp_n_files,save_to_filename='test_topology.yaml')
