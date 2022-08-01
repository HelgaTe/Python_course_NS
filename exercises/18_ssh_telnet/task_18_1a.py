# -*- coding: utf-8 -*-
"""
Задание 18.1a

Скопировать функцию send_show_command из задания 18.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется при ошибке аутентификации
на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
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
    except netmiko.NetmikoAuthenticationException as err:
        print(err)


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
        # pprint(devices)

    for dev in devices:
        pprint(send_show_command(dev, command))
