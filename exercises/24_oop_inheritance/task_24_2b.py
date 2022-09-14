# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

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

    def send_command(self, command, **kwargs):
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
    print(r1.send_command('sh ip br'))
