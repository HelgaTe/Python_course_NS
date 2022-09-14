# -*- coding: utf-8 -*-

"""
Задание 24.2c

Скопировать класс MyNetmiko из задания 24.2b.
Проверить, что метод send_command кроме команду, принимает еще и дополнительные
аргументы, например, strip_command.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал
любые аргументы, которые поддерживает netmiko.


In [2]: from task_24_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""

from netmiko.cisco.cisco_ios import CiscoIosSSH
import re


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs)  # инициализировать все переменные родительского класса, которые переданы как ключевые аргументы
        self.enable()  # ssh >>> self (from parent class)

    def send_command(self, command, *args, **kwargs):
        output = super().send_command(command, **kwargs)
        self._check_error_in_command(command, output)
        return output

    def send_config_set(self, commands):
        if type(commands) == str:
            commands = [commands]
        comm_output = ''
        self.config_mode()
        for cmd in commands:
            result = super().send_config_set(cmd, exit_config_mode=False)
            comm_output += result
            self._check_error_in_command(cmd, result)
        self.exit_enable_mode()
        return comm_output

    def _check_error_in_command(self, command, com_output):
        if '%' in com_output:
            error = re.search(r'%.+', com_output).group()
            raise ErrorInCommand(
                f'При выполнении команды "{command}" на устройстве {self.host} возникла ошибка "{error}"')


if __name__ == '__main__':
    device_params = {
        "device_type": "cisco_ios",
        "ip": "172.16.100.130",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }

    r1 = MyNetmiko(**device_params)
    print(r1.send_command('sh ip int br', strip_command=False))
    print(r1.send_command('sh ip int br', strip_command=True))
