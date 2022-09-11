from cisco_telnet_base import BaseTelnet


class CiscoTelnet(BaseTelnet):  # child class some features are inherited from parent class(BaseTelnet)
    def __init__(
            self, ip, username, password, secret, short_sleep=1, long_sleep=5
    ):  # inherite __init__ from parent class
        super().__init__(ip, username, password, short_sleep, long_sleep)
        # BaseTelnet.__init__(self, ... ) # после super мы унаследовали все переменные в __init__в т.ч. self._telnet (у нас есть сессия, с которой мы будем работать)
        self._telnet.write(b'enable\n')
        self._telnet.read_until(b'Password')
        self._telnet.write(secret.encode('utf-8') + b'\n')

    def send_config(self, commands):
        self._telnet.write(b'conf t\n')
        output = self._telnet.read_until(b'#\n')
        output += super().send_command(commands)
        self._telnet.write(b'end\n')
        output += self._telnet.read_until(b'#\n')
        return output

    def get_config(self,command='sh run'):
        return self.send_command(command)

if __name__ == "__main__":
    with CiscoTelnet("172.16.100.129", "cisco", "cisco", "cisco") as r1:
        # print(r1.send_command('sh ip int br'))

        # print(r1.send_config(['conf t', 'logging 10.1.1.1', 'end'])) # def send_config taken from parent class, w/o modification
        # print(r1.send_config('logging 10.1.1.1'))
        print(r1.get_config())