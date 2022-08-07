import logging
from datetime import datetime
from pprint import pprint

import netmiko
import yaml

# эта строка указывает, что лог-сообщения paramiko будут выводиться только если они уровня WARNING и выше
# т.е. инфо сообщения модуля paramiko будут игнорироваться
logging.getLogger("paramiko").setLevel(logging.WARNING) # name of the module that creates a log + logging level

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def send_show(device, show):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device["host"]
    logging.info(start_msg.format(datetime.now().time(), ip))

    with netmiko.ConnectHandler(**device) as ssh:
        result={}
        ssh.enable()
        output = ssh.send_command(show)
        result[ip]=output
        logging.info(received_msg.format(datetime.now().time(), ip))
    return result


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    for dev in devices:
        pprint(send_show(dev, 'sh clock'))
