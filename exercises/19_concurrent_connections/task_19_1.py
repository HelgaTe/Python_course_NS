# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
import subprocess
from concurrent.futures import ThreadPoolExecutor

from pprint import pprint


def ping_ip(ip):
    '''
    функция проверяет пингуются ли IP-адреса.
    @param ip: ip address to ping
    @return: True, False value (reachable or unreachable)
    '''
    result = subprocess.run(
        ['ping', '-c', '3', '-n', ip],
        stdout=subprocess.PIPE)
    ip_reachable=result.returncode==0
    return ip_reachable # True, False value


def ping_ip_addresses (ip_list,limit=3):
    '''
    функция проверяет пингуются ли IP-адреса
    @param ip_list: список IP-адресов
    @param limit: максимальное количество параллельных потоков (по умолчанию 3)
    @return: кортеж с двумя списками: список доступных IP-адресов и список недоступных IP-адресов
    '''
    reachable_list = []
    unreachable_list = []
    with ThreadPoolExecutor (max_workers=limit) as executor:
        output=executor.map(ping_ip,ip_list)
        for ip,status in zip(ip_list,output):
            if status:
                reachable_list.append(ip)
            else:
                unreachable_list.append(ip)
    return reachable_list, unreachable_list

if __name__ == '__main__':
    print(ping_ip_addresses(["8.8.8.8", "192.168.100", "192.168.100.1"],limit=2))