# -*- coding: utf-8 -*-
"""
Задание 18.1b

Скопировать функцию send_show_command из задания 18.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется при ошибке
аутентификации на устройстве, но и исключение, которое генерируется, когда IP-адрес
устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
"""
import netmiko
import yaml
from pprint import pprint

def send_show_command (device, command):
    '''
    подключается по SSH и выполняет указанную команду
    @param device: словарь с параметрами подключения к устройству
    @param command:  команда, которую надо выполнить
    @return:
    '''

    try:
        with netmiko.ConnectHandler(**device) as ssh: # Подключение по SSH, распаковка параметров
            ssh.enable() # Перейти в режим enable
            output=ssh.send_command(command) # отправить одну команду
        return output
    except (netmiko.NetmikoAuthenticationException,netmiko.NetmikoTimeoutException) as err:
        print(err)


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_show_command(dev, command))
