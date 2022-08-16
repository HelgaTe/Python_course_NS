# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""
import textfsm
from pprint import pprint


def parse_output_to_dict(template, command_output):
    with open(template) as f:  # считать содержимое файлов (template & output data)
        re_table = textfsm.TextFSM(f)  # класс обрабатывает шаблон и создает из него объект в TextFSM
        key = re_table.header  # отобрать заголовки таблиц
        value = re_table.ParseText(command_output)  # передать содержимое файла с output data в шаблон
    return [dict(zip(key, v)) for v in value]


if __name__ == '__main__':
    templ = 'templates/sh_ip_int_br.template'
    output = 'output/sh_ip_int_br.txt'

    with open(output) as f:
        comm_output = f.read()
        # считать вывод команды, который записан в файле в строку, т.к. параметром функции есть именно строка
        print(parse_output_to_dict(templ, comm_output))
