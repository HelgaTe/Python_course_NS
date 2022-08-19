import telnetlib
import time

# используя функции из файла cisco_telnet_fucntions.py преобразование функции в класс

class CiscoTelnet:
    """
    сделанные преобразования :
        имя функции не func connect а func __init__
        добавить аргумент self
        убрать return (в __init__ не используется)
    """
    def __init__(
        self, ip, username, password, enable_password=None, disable_paging=True
    ):
        self.ip = ip
        self.username = username

        self._telnet = telnetlib.Telnet(ip)
        self._telnet.read_until(b"Username:")
        self._telnet.write(username.encode("ascii") + b"\n")
        self._telnet.read_until(b"Password:")
        self._telnet.write(password.encode("ascii") + b"\n")
        if enable_password:
            self._telnet.write(b"enable\n")
            self._telnet.read_until(b"Password:")
            self._telnet.write(enable_password.encode("ascii") + b"\n")
        if disable_paging:
            self._telnet.write(b"terminal length 0\n")
        time.sleep(0.5)
        self._telnet.read_very_eager()

    def send_show_command(self, command): # создаем методы работы с экземплярами класса
        self._telnet.write(command.encode("utf-8") + b"\n")
        output = self._telnet.read_until(b"#").decode("utf-8")
        return output

    def _read_until_prompt(self, prompt="#"):
        return self._telnet.read_until(prompt.encode("utf-8")).decode("utf-8")

    def send_config(self, commands):
        if type(commands) == str:
            commands = ["conf t", commands, "end"] # зайти / выйти с режима конфигурации (чтобы избежать ошибок при вызове sh команд, если их надо потом выполнить)
        else:
            commands = ["conf t", *commands, "end"] # * - распаковать список  или кортеж, если команда передана не как строка
        output = "" # собрать результаты вывода в строку
        for cmd in commands:
            self._telnet.write(cmd.encode("utf-8") + b"\n")
            output += self._read_until_prompt()
        return output

    def close(self):
        self._telnet.close() # close current session

    def get_cfg(self, command="sh run"): # 'sh run' is set be default ('sh start' - as an option)
        return self.send_show_command(command) # используем метод send_show_command из данного класса, поэтому пишем через self



if __name__ == "__main__":
    r1 = CiscoTelnet("172.16.100.129", "cisco", "cisco", "cisco")
    r1.send_show_command("sh clock")
    # CiscoTelnet.send_show_command(r1, "sh clock")

    r1 = CiscoTelnet("172.16.100.130", "cisco", "cisco", "cisco")  # установить подключение с оборудованием
    # print(r1)
    """
    output : <__main__.CiscoTelnet object at 0x7f8912118110>
    """
    sh_com = r1.send_show_command('sh clock')  # применить метод send_show_command к текущему подключению
    # print(sh_com)
    """
    output :
        sh clock
        *18:42:01.379 UTC Sun Aug 14 2022
        R1#
    """
    cfg_com = r1.send_config(['int Lo0', 'desc TEST'])  # применить метод send_config к текущему подключению
    # print(cfg_com)
    """
    output:
        conf t
        Enter configuration commands, one per line.  End with CNTL/Z.
        R1(config)#int Lo0
        R1(config-if)#desc TEST
        R1(config-if)#end
        R1#
    """
    get_out = r1.get_cfg('sh start')
    # print(get_out)