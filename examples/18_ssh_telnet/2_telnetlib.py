import telnetlib
import time
from pprint import pprint


def to_bytes(line):
    '''
    функция выполняет преобразование в байты и добавление перевода строки
    @param line: simple line
    @return: byte str
    '''
    return f"{line}\n".encode("utf-8")


def send_show_command(ip, username, password, enable, commands):
    with telnetlib.Telnet(ip) as telnet: # выполнение подключения
        telnet.read_until(b"Username") # до какой строки считать вывод
        telnet.write(to_bytes(username)) # передать данные
        telnet.read_until(b"Password")
        telnet.write(to_bytes(password))
        index, m, output = telnet.expect([b">", b"#"]) # позволяет указывать список с регулярными выражениями

        if index == 0:
            telnet.write(b"enable\n")
            telnet.read_until(b"Password")
            telnet.write(to_bytes(enable))
            telnet.read_until(b"#", timeout=5)
        telnet.write(b"terminal length 0\n")
        telnet.read_until(b"#", timeout=5)
        time.sleep(3)
        telnet.read_very_eager() # отправить несколько команд, а затем считать весь доступный вывод

        result = {}
        for command in commands:
            telnet.write(to_bytes(command))
            output = telnet.read_until(b"#", timeout=5).decode("utf-8")
            result[command] = output.replace("\r\n", "\n")
        return result


if __name__ == "__main__":
    devices = ["172.16.100.129", "172.16.100.130", "172.16.100.131"]
    commands = ["sh ip int br", "sh arp"]
    for ip in devices:
        result = send_show_command(ip, "cisco", "cisco", "cisco", commands)
        pprint(result, width=120)
