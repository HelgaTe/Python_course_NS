# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
import ipaddress


class IPAddress:
    def __init__(self, ipaddress):
        ip, mask = ipaddress.split('/')
        self.ip = self._correct_ip(ip)
        self.mask = self._correct_mask(mask)
        self.mask = int(mask)
        self.ipaddress=ipaddress

    def _correct_mask(self, mask):
        if mask.isdigit() and int(mask) in range(8, 33):
            return True
        else:
            raise ValueError('Incorrect mask')

    def _correct_ip(self, ip):
        octets = ip.split('.')
        correct_octets = [oct for oct in octets if oct.isdigit() and int(oct) in range(226)]
        if len(octets) == 4 and len(correct_octets) == 4:
            return ','.join(correct_octets).replace(',', '.')
        else:
            raise ValueError('Incorrect IPv4 address')

    def __str__(self):
        return f'IP address {self.ipaddress}'

    def __repr__(self):
        return f"IPAddress('{self.ipaddress}')"




if __name__ == '__main__':
    ip1 = IPAddress('10.1.1.1/24')
    ip2 = IPAddress('100.1.1.1/24')
    print(ip1)
    print(ip2)
    ip_list=[]
    ip_list.append(ip1)
    ip_list.append(ip2)
    print(ip_list)


