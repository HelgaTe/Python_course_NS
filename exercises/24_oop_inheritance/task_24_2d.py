# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_command(self, command, *args, **kwargs):
        output = super().send_command(command, **kwargs)
        self._check_error_in_command(command, output)
        return output

    def send_config_set(self, commands, ignore_errors = True, *args, **kwargs):
        if ignore_errors:
            output = super().send_config_set(commands,*args,**kwargs)
            return output
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
