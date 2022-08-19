class IPAddress:
    """
    Класс IPAddress
    """
    def __int__(self, ip, mask): # метод __init__ чтобы передать переменные
        """
        Параметры ip, mask (instance variables)
        """
        self.ip = ip
        self.mask = mask

    def bin(self): # дальше при создании методов - обращаться к абстрактному экземпляру, который определен в __init__
        """
        Конвертация ip в bin (method)
        """
        octets=[int(o) for o in self.ip.split('.')]
        bin_str=("{:08b}"*4).format(*octets)
        return bin_str


ip1 = IPAddress() # определить класс -> шаблон для создания объекта (описывает тип данных)
ip1.ip='172.100.16.130' # передать начальные данные
ip1.mask=24 # передать начальные данные

print(ip1.ip) # вывести значение переменной
print(str('='*32))
print(ip1.bin()) # преобразовать изначальные данные в двоичный формат

'''
Docstring output 
    In [16]: ip1.bin?
    
    Signature: ip1.bin()
    Docstring: Конвертация ip в bin
    File:      ~/Documents/Python_2021/Python_summer2021/examples/22_oop_basics/very_basic_oop.py
    Type:      method
'''

