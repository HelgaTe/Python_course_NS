import ipaddress
from operator import add


class Network:
    def __init__(self, network, mask):
        self.network = network
        self.mask = mask
        ipv4net = ipaddress.ip_network(f'{self.network}/{self.mask}')
        self.hosts = [str(ip) for ip in ipv4net.hosts()]

    def __str__(self):
        return f'{self.network}, {self.mask}'

    def __repr__(self):
        return f'Network({self.network}, {self.mask})'

    def __len__(self):
        return len(self.hosts)

    def __getitem__(self, index):  # возможность возвращаться к элементам итерируемого объекта по индексу
        print('__getitem__')  # support line, can be omitted
        return self.hosts[index]

    def __iter__(self):
        print('__iter__')
        return iter(self.hosts)  # iterator


class Repeat:  # свой класс, который является итератором
    def __init__(self, value):
        self.value = value

    def __next__(self):
        return self.value

    def __iter__(self):
        return self


class Range:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self._last = start

    def __next__(self):
        print('__next__')
        value = self._last
        if value == self.stop:
            raise StopIteration
        self._last += 1
        return value

    def __iter__(self):  # чтобы рабол цикл for
        print('__iter__')
        return self


if __name__ == '__main__':
    net1 = Network('10.1.1.0', 29)
    print(net1)
    print(net1.hosts)
    print(net1[0:4])  # __getitem__

    for ip in net1:
        print(ip)

    print(list(zip([1, 2, 3], Repeat(1000))))
    print(list(map(add, [1, 2, 3], Repeat(1000))))

    w = Range(1, 9)
    for i in w:
        print(i)
