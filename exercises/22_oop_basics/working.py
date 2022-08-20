from pprint import pprint

data = {('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
        ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
        ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
        ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
        ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
        ('R3', 'Eth0/2'): ('R3', 'Eth0/2')}


def add_link(top,add1,add2):
        n_top = top.copy()
        for i in n_top.items():
                if add1 in i or add2 in i:
                        print('Cоединение с одним из портов существует')
                elif add1 in i and add2 in i :
                        print('Такое соединение существует')
                else:
                        new_link = {add1: add2}
                        top.update(new_link)


add1 = ('R3', 'Eth0/2')
add2 = ('R3', 'Eth0/2')

pprint(add_link(data,add1,add2))
