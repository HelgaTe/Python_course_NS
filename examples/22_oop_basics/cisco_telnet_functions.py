import telnetlib
import time


def _check_errors(command_output):
    if "Invalid input detected" in command_output:
        raise ValueError("Возникла ошибка Invalid input detected")


def connect(ip, username, password, enable_password=None, disable_paging=True):
    """
     func делает подключение и возвращает подключение под именем telnet
     не через менеджер контекста (with open) - чтобы сессия автоматически не закрывалась
     и данное подключение можно было использовать для других действий с экземпляром
    """
    telnet = telnetlib.Telnet(ip)
    telnet.read_until(b"Username:")
    telnet.write(username.encode("ascii") + b"\n")
    telnet.read_until(b"Password:")
    telnet.write(password.encode("ascii") + b"\n")
    if enable_password:
        telnet.write(b"enable\n")
        telnet.read_until(b"Password:")
        telnet.write(enable_password.encode("ascii") + b"\n")
    if disable_paging:
        telnet.write(b"terminal length 0\n")
    time.sleep(0.5)
    telnet.read_very_eager()
    return telnet


def send_show_command(connection, command): # переменная connection - это созданное подключение с func выше
    '''
    используя готовое соединение connection, которое ожидается как первый аргумент данной функции,
    вторым аргументом передаем команду, которую надо выполнить
    '''

    connection.write(command.encode("ascii") + b"\n")
    time.sleep(1)
    output = connection.read_very_eager().decode("ascii")
    return output


def send_config_commands(connection, commands):  # аналогично как для sh command
    connection.write("conf t".encode("ascii") + b"\n")
    for command in commands:
        connection.write(command.encode("ascii") + b"\n")
        time.sleep(0.2)
    output += telnet.read_very_eager().decode("ascii")
    connection.write("end".encode("ascii") + b"\n")
    return output


if __name__ == "__main__":
    r1 = connect("172.16.100.129", "cisco", "cisco", "cisco") # создать подключение и записать в переменную r1 - дальше используем эту переменную для запуска команд
    sh_ip_int_br = send_show_command(r1, "sh ip int br") # используя подключение к оборудованию (r1), выполнить заданную sh command
    print(sh_ip_int_br)
    """
    output :
        sh ip int br
        Interface                  IP-Address      OK? Method Status                Protocol
        FastEthernet0/0            172.16.100.129  YES DHCP   up                    up      
        FastEthernet0/1            unassigned      YES NVRAM  administratively down down    
        R1#
    """

    out = send_show_command(r1, "sh version")
    print(out)
    r1.close() # закрыть текущую сессию подключение (def connect - создана не через менеджер контекста)