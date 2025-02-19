import re
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
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect(
        hostname=ip,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False,
    )
    with cl.invoke_shell() as ssh:
        ssh.send("enable\n")
        ssh.send(enable + "\n")
        time.sleep(short_pause)
        ssh.recv(max_bytes)

        result = {}
        for command in commands:
            ssh.send(f"{command}\n")
            ssh.settimeout(5)

            output = ""
            while True:
                try:
                    page = ssh.recv(max_bytes).decode("utf-8")
                    output += page
                    time.sleep(0.5)
                except socket.timeout:
                    break
                if "More" in page:
                    ssh.send(" ")
            output = re.sub(" +--More--| +\x08+ +\x08+", "\n", output)
            result[command] = output

        return result


if __name__ == "__main__":
    devices = ["172.16.100.129", "172.16.100.130", "172.16.100.131"]
    commands = ["sh run"]
    result = send_show_command("172.16.100.129", "cisco", "cisco", "cisco", commands)
    pprint(result, width=120)
