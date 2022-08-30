# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить
метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей,
  полученный после обработки с помощью TextFSM.
  При parse=True должен возвращаться список словарей, а parse=False обычный вывод.
  Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status
Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up
up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up...'


"""
import telnetlib
from textfsm import clitable


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):  # create and assign variables
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret

    def _write_line(self, line):  # convert line into byte line
        b_line = f'{line}\n'.encode('utf-8')
        return b_line

    def send_show_command(self, command, parse=True, templates='templates', index='index'):
        with telnetlib.Telnet(self.ip) as self._telnet:
            self._telnet.read_until(b'Username')
            self._telnet.write(self._write_line(self.username))
            self._telnet.read_until(b'Password')
            self._telnet.write(
                self._write_line(self.password))  # установлено подключение к оборудованию (передано ip, passwd)
            indx, m, output = self._telnet.expect([b">", b"#"])
            # return indx, m, output
            if indx == 0:  # если метод expect вернул 0, то совпадение было найдено (это элемент с индексом ноль)
                self._telnet.write(self._write_line('enable'))
                self._telnet.read_until(b'Password')
                self._telnet.write(self._write_line(self.secret))
                self._telnet.read_until(b'#')
                self._telnet.write(self._write_line(command))  # передать команду
                com_output = self._telnet.read_until(b'#').decode('utf-8')
            if not parse:
                return com_output
            attributes = {"Command": command, "Vendor": "cisco_ios"}
            cli_table = clitable.CliTable(index, templates)
            cli_table.ParseCmd(com_output, attributes)
            k = cli_table.header
            comm_dict = [dict(zip(k, v)) for v in cli_table]
            return comm_dict


if __name__ == '__main__':
    r1 = CiscoTelnet("172.16.100.129", "cisco", "cisco", "cisco")
    print(r1.send_show_command('sh ip interface brief'))
