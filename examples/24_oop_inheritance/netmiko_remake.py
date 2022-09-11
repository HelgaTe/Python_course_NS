# переделать или дописать готовый класс, чтобы он удовлетворял наши потребности

from netmiko.cisco.cisco_ios import CiscoIosSSH

# создать свой класс Исключений : создать свой класс и наследовать Exception
class NetworkErrorInCommand(Exception):
    """Исключение генерируется при ошибке в команедах на сетевом оборудовании"""



class MyNetmiko(CiscoIosSSH):
    # ssh >>> self (from parent class)
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs)  # инициализировать все переменные родительского класса, которые переданы как ключевые аргументы
        print(self.find_prompt())  # stdout : R2>

    def send_command(self, command, **kwargs):
        output = super().send_command(command, **kwargs)
        if '%' in output:
            # print(f'Возникла ошибка при выполнении команды {command} на оборудовании {self.host}')
            # raise ValueError (f'Возникла ошибка при выполнении команды {command} на оборудовании {self.host}')
            raise NetworkErrorInCommand(f'Возникла ошибка при выполнении команды {command} на оборудовании {self.host}')
        return output



if __name__ == '__main__':
    device_params = {
        "device_type": "cisco_ios",
        "ip": "172.16.100.130",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }

    r1 = MyNetmiko(**device_params)
    print(r1.send_command('sh ip intf br'))



