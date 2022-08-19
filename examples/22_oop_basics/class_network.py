import ipaddress


class Network:
    all_allocated_ip = [] # переменная класса, тут будут содержаться все выделенные адреса (для всех сетей)

    def __init__(self, network, mask): # через __init__ создаем переменные экземпляра класса
        self.network = network
        self.mask = mask
        self.allocated = [] # переменная экземпляра, тут будут содержаться выделенные адреса конкретной сети
        ipv4net = ipaddress.ip_network(f"{self.network}/{self.mask}")
        self.hosts = [str(ip) for ip in ipv4net.hosts()]

    def allocate_ip(self, ip):
        if ip in self.hosts:
            if ip not in self.allocated:
                self.allocated.append(ip)
                # Network.all_allocated_ip.append(ip)
                '''
                лучше записывать через имя класса, а не через self потому, что экземпляр может создавать 
                имена переменных, как имена переменных класса и в этом случае можно перезаписать данные 
                класса и при вызове их через конкретный экземпляр значения переменных класса будут 
                недоступны, но по прежнему доступны через класс или другой экземпляр класса
                '''
                type(self).all_allocated_ip.append(ip)
            else:
                raise ValueError(
                    f"IP-адрес {ip} уже находится в allocated "
                    f"\n{self.allocated}"
            )
        else:
            raise ValueError(
                f"IP-адрес {ip} не входит в сеть {self.network}/{self.mask}"
            )

    def __str__(self): # вывести читабельное информационное сообщение для пользователя
        return f"{self.network}/{self.mask}"

    def __repr__(self): # возвращает печатное представление данного класса (чтобы получить детали по объекту, бльше дляпрограммиста)
        return f"Network('{self.network}', {self.mask})"

    def __len__(self): # сделать так, чтобы в нашем классе были доступны методы стандартных классов
        return len(self.hosts)


if __name__=='__main__':
    n1=Network('10.1.192.0',29)
    print(type(n1)) # output : <class '__main__.Network'>
    print(n1) # output : 10.1.1.0/29
    print(n1.hosts) # output : ['10.1.192.1', '10.1.192.2', '10.1.192.3', '10.1.192.4', '10.1.192.5', '10.1.192.6']
    print(len(n1.hosts))  # output : 6

