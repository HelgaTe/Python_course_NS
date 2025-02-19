# -*- coding: utf-8 -*-
"""
Задание 21.1

Создать функцию parse_command_output. Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды sh ip int br с оборудования
и шаблоне templates/sh_ip_int_br.template.

"""
from netmiko import ConnectHandler
import textfsm

def parse_command_output (template, command_output):
    with open (template) as f:
        fsm_obj=textfsm.TextFSM(f)
        header=fsm_obj.header
        tab_values=fsm_obj.ParseText(command_output)
    return [header]+tab_values



# вызов функции должен выглядеть так
if __name__ == "__main__":
    r1_params = {
        "device_type": "cisco_ios",
        "host": "172.16.100.129",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with ConnectHandler(**r1_params) as r1:
        r1.enable()
        output = r1.send_command("sh ip int br")
        # сгенерировать вывод команды предварительно подключившись к оборудованию по SSH и передать этот вывод
        # print(output)
    result = parse_command_output("templates/sh_ip_int_br.template", output)
    print(result)
