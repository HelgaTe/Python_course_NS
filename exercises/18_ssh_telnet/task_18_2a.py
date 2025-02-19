# -*- coding: utf-8 -*-
"""
Задание 18.2a

Скопировать функцию send_config_commands из задания 18.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода информация о том
к какому устройству выполняется подключение.
По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства
из файла devices.yaml с помощью функции send_config_commands.
"""

import netmiko
import yaml


def send_config_commands(device,config,log=True):
    '''
    подключается по SSH к устройству и выполняет перечень команд в конфигурационном режиме
    @param device: словарь с параметрами подключения к устройству
    @param config: список команд, которые надо выполнить
    '''
    with netmiko.ConnectHandler(**device) as ssh:
        if log:
            log=device['host']
            status=f'Подключаюсь к {log}'
            print(status)
        ssh.enable()
        output=ssh.send_config_set(config)
    return output



if __name__ == "__main__":

    commands = ['logging 10.255.255.1', 'logging buffered 20010', 'no logging console']

    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    for device in devices:
        print(send_config_commands (device, commands))
