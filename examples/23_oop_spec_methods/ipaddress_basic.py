import ipaddress
import os


class IPAddress:
    def __init__(self, ip):
        self.ip = ip

    def __repr__(self):
        return f'IPAddress({self.ip})'

    def __add__(self, num):  # получить новый ip через прибавление числа к существующему ip
        if type(num) != int:
            raise TypeError(f'Can only concatenate int (not {type(num).__name__})')
        ip_as_int = int(self)  # __int__
        result_ip_int = ip_as_int + num
        result_ip_str = str(ipaddress.ip_address(
            result_ip_int))  # получим строку вида '10.1.1.1', но нужен экземпляр класса IP -> в return преобразование
        return IPAddress(result_ip_str)

    def __lt__(self, other):  # оператор сравнения: больше/ меньше; сортировка
        if type(other) != IPAddress:
            raise TypeError(f'Can only compare int (not {type(other).__name__})')
        return int(self) < int(other)

    def __int__(self):  # инициализировать стандартный метод int для данного класса
        ip_as_int = int(ipaddress.ip_address(self.ip))
        return ip_as_int

    def __eq__(self, other):
        if type(other) != IPAddress:
            raise TypeError(f'Can only concatenate int type (not {type(other).__name__})')
        return self.ip == other.ip

    def __le__(self, num):  # сравнить больше или равно/ меньше или равно
        if type(num) != IPAddress:
            raise TypeError(f'Can only concatenate int type (not {type(num).__name__})')
        return int(self) <= int(num)


if __name__ == '__main__':  # __name__ >>> определенная часть кода должна выполняться, когда модуль выполняется напрямую (не через импорт)

    # ip1 = IPAddress('10.10.1.1')
    # ip2 = ip1 + []  # использование __add__
    # print(ip1)
    # print(ip2)

    ip3 = IPAddress('10.1.1.1')
    ip4 = IPAddress('10.1.1.11')
    ip5 = IPAddress('10.1.1.10')
    ip6 = IPAddress('10.1.1.2')
    ip7 = IPAddress('10.1.1.1')
    ip_list = [ip3, ip4, ip5, ip6]
    print(ip3 < ip4)
    print(ip_list)
    print(ip3 == ip7)  # __eq__ (оператор сравнения)
    print(ip3 != ip7)  # обратные методы доступны также
    print(sorted(ip_list))  # __lt__ (оператор сортировки)

    print(os.path.abspath('ipaddress_basic.py'))  # переменная __file__ полезна в определении текущего пути к файлу
    """
    stdout = /Users/Olha/Documents/Python_2021/Python_summer2021/examples/23_oop_spec_methods/ipaddress_basic.py
    """