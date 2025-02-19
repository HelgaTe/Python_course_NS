# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

template='''
{:<25}{}
{:<25}{}
{:<25}{}
{:<25}{}
{:<25}{}
'''

with open('ospf.txt','r') as f:
    for line in f:
        line=line.rstrip()
        line=line.split()
        param1=line[1]
        param2=line[2].strip('[').strip(']')
        param3=line[4].strip(',')
        param4=line[5].strip(',')
        param5=line[6]
        print(template.format('Prefix',param1,'AD/Metric',param2,'Next-Hop',param3,'Last update',param4,'Outbound Interface',param5))
