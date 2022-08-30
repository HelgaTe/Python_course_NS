# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""

import telnetlib
from textfsm import clitable
import time

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        '''
        инициализировать подключение, НЕ через менеджер контекста - потому, что сессия должна быть открыта
        т.к. надо запускать разные команды в рамках одной сессии и потом явно закрыть сессию по завершению
            def connection -> def __init__ (examples >> cisco_telnet_functions/class)
        '''
        self.telnet=telnetlib.Telnet(ip) # выполнить подключение и записать в переменную telnet через self, чтобы она была доступна при дальнейшей работе
        self.telnet.read_until(b"Username:")
        self._write_line(username)
        self.telnet.read_until(b"Password:")
        self._write_line(password)
        self._write_line("enable")
        self.telnet.read_until(b"Password:")
        self._write_line(secret)
        time.sleep(1) # перед read_very_eager всегда надо делать sleep иначе он мгновенно после отправки команды читает вывод, а там еще ничего нет и так как он не ждет приглашения, то на этом он и останавливается
        self.telnet.read_very_eager() # отправить несколько команд, затем считать весь доступный вывод


    def _write_line(self, line):
        '''
        func is used to convert str into byte str
        self.telnet - переменная, которая определена в func __init__
        в обычной функции записано так: telnet.write(b'cisco\n')
        '''
        self.telnet.write(line.encode('utf-8') + b'\n')

    def send_show_command(self, command, parse=True, templates='templates', index='index'):
        self._write_line(command)  # передать команду,первый аргумент метода (self) - инициализированное подключение (func __init__)
        time.sleep(1)
        sh_output = self.telnet.read_very_eager().decode('utf-8')
        if not parse:
            return sh_output
        attributes = {"Command": command, "Vendor": "cisco_ios"}
        cli_table = clitable.CliTable(index, templates)
        cli_table.ParseCmd(sh_output, attributes)
        k = cli_table.header
        comm_dict = [dict(zip(k, v)) for v in cli_table]
        return comm_dict

    def send_config_commands (self, commands):
        if type(commands)==str:
            commands=['conf t', commands, 'end']
        else:
            commands=['conf t', *commands, 'end']
        cnfg_output=''
        for cmd in commands:
            self._write_line(cmd)
            cnfg_output +=self.telnet.read_until(b'#').decode('utf-8')
        return cnfg_output




if __name__ == '__main__':
    r1 = CiscoTelnet("172.16.100.129", "cisco", "cisco", "cisco")
    print(r1.send_show_command('sh ip interface brief'))
    print(r1.send_show_command("sh clock", parse=False))
    print(r1.send_config_commands(['ip address 5.5.5.5 255.255.255.255']))
