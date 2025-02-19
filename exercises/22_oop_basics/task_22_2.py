# -*- coding: utf-8 -*-

"""
Задание 22.2

Создать класс CiscoTelnet, который подключается по Telnet к оборудованию Cisco.

При создании экземпляра класса, должно создаваться подключение Telnet, а также
переход в режим enable.
Класс должен использовать модуль telnetlib для подключения по Telnet.

У класса CiscoTelnet, кроме __init__, должно быть, как минимум, два метода:
* _write_line - принимает как аргумент строку и отправляет на оборудование строку
  преобразованную в байты и добавляет перевод строки в конце. Метод _write_line должен
  использоваться внутри класса.
* send_show_command - принимает как аргумент команду show и возвращает вывод
  полученный с обрудования

Параметры метода __init__:
* ip - IP-адрес
* username - имя пользователя
* password - пароль
* secret - пароль enable

Пример создания экземпляра класса:
In [2]: from task_22_2 import CiscoTelnet

In [3]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}
   ...:

In [4]: r1 = CiscoTelnet(**r1_params)

In [5]: r1.send_show_command("sh ip int br")
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                unassigned      YES manual up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nR1#'


Подсказка:
Метод _write_line нужен для того чтобы можно было сократить строку:
self.telnet.write(line.encode("ascii") + b"\n")

до такой:
self._write_line(line)

Он не должен делать ничего другого.
"""

import telnetlib


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):  # create and assign variables
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret

    def _write_line(self, line):  # convert line into byte line
        b_line = f'{line}\n'.encode('utf-8')
        return b_line

    def send_show_command(self, command):
        with telnetlib.Telnet(self.ip) as self._telnet:
            self._telnet.read_until(b'Username')
            self._telnet.write(self._write_line(self.username))
            self._telnet.read_until(b'Password')
            self._telnet.write(self._write_line(self.password))  # установлено подключение к оборудованию (передано ip, passwd)
            indx, m, output = self._telnet.expect([b">", b"#"])
            # return indx, m, output
            if indx == 0:  # если метод expect вернул 0, то совпадение было найдено (это элемент с индексом ноль)
                self._telnet.write(self._write_line('enable'))
                self._telnet.read_until(b'Password')
                self._telnet.write(self._write_line(self.secret))
                self._telnet.read_until(b'#')
                self._telnet.write(self._write_line(command))
                com_output = self._telnet.read_until(b'#')
            return com_output.decode('utf-8')


if __name__ == '__main__':
    r1 = CiscoTelnet("172.16.100.129", "cisco", "cisco", "cisco")
    print(r1.send_show_command('sh clock'))
