import socket
import time
from pprint import pprint

import paramiko


def send_show_command(
    ip,
    username,
    password,
    enable,
    command,
    max_bytes=60000,
    short_pause=1,
    long_pause=5,
):
    '''
    сначала создается клиент и выполняются настройки клиента,
    затем выполняется подключение и получение интерактивной сессии
    '''
    cl = paramiko.SSHClient() # класс, который представляет соединение к SSH-серверу, выполняет аутентификацию клиента
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # настройка указывает какую политику использовать, когда выполнятся подключение к серверу, ключ которого неизвестен. Политика paramiko.AutoAddPolicy() автоматически добавляет новое имя хоста и ключ в локальный объект HostKeys.
    cl.connect(
        hostname=ip,
        username=username,
        password=password,
        look_for_keys=False, # по умолчанию аутентификация по ключам. Чтобы отключить - поставить флаг False
        allow_agent=False, # может подключаться к локальному SSH агенту ОС. Это нужно при работе с ключами; в данном случае аутентификация по логину/паролю (нужно отключить)
    ) # выполняет подключение к SSH-серверу и аутентифицирует подключение
    with cl.invoke_shell() as ssh: # установить интерактивную сессию SSH с сервером
        ssh.send("enable\n")
        ssh.send(enable + "\n")
        time.sleep(short_pause)
        ssh.send("terminal length 0\n")
        time.sleep(short_pause)
        ssh.recv(max_bytes)

        result = {}
        for command in commands:
            ssh.send(f"{command}\n")
            ssh.settimeout(5)

            output = ""
            while True:
                try:
                    part = ssh.recv(max_bytes).decode("utf-8")
                    output += part
                    time.sleep(0.5)
                except socket.timeout:
                    break
            result[command] = output

        return result


if __name__ == "__main__":
    devices = ["172.16.100.129", "172.16.100.130", "172.16.100.131"]
    commands = ["sh clock", "sh arp"]
    result = send_show_command("172.16.100.129", "cisco", "cisco", "cisco", commands)
    pprint(result, width=120)
