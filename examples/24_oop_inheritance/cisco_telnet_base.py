import telnetlib
import time


class BaseTelnet:  # parent class >> basic connection to device by ssh
    print('BaseTelnet __init__')

    def __init__(self, ip, username, password, short_sleep=1, long_sleep=5):
        self.ip = ip
        self.username = username
        self.short_sleep = short_sleep
        self.long_sleep = long_sleep
        self._telnet = telnetlib.Telnet(ip)
        self._telnet.read_until(b"Username:")
        self._telnet.write(username.encode("utf-8") + b"\n")
        self._telnet.read_until(b"Password:")
        self._telnet.write(password.encode("utf-8") + b"\n")
        time.sleep(self.short_sleep)
        self._telnet.read_very_eager()

    def send_command(self, command):
        self._telnet.write(command.encode("utf-8") + b"\n")
        time.sleep(self.long_sleep)
        output = self._telnet.read_very_eager().decode("utf-8")
        return output.replace('\r\n', '\n')

    def _read_until_prompt(self, prompt="#"):
        return self._telnet.read_until(prompt.encode("utf-8")).decode("utf-8")

    def send_config(self, commands):
        if type(commands) == str:
            commands = [commands]
        else:
            commands = [*commands]
        output = ""
        for cmd in commands:
            self._telnet.write(cmd.encode("utf-8") + b"\n")
            time.sleep(self.short_sleep)  # <variable from __init__ is not working>
            output += self._telnet.read_very_eager().decode('utf-8')
        return output.replace('\r\n', '\n')

    def close(self):
        self._telnet.close()

    def __enter__(self):  # to enable <contex manager (with)>
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # to enable <contex manager (with)>
        self.close()





if __name__ == "__main__":
    with BaseTelnet("172.16.100.129", "cisco", "cisco") as r1:
        print(r1.send_command('sh clock'))
