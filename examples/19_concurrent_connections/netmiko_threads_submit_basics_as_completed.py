import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pprint import pprint

import yaml
from netmiko import ConnectHandler, NetMikoAuthenticationException

logging.getLogger("paramiko").setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def send_show(device_dict, command):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received: {}'
    ip = device_dict['host']
    logging.info(start_msg.format(datetime.now().time(), ip))
    if ip == '172.16.100.129':
        time.sleep(5)

    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        logging.info(received_msg.format(datetime.now().time(), ip))
    return {ip: result}


with open('devices.yaml') as f:
    devices = yaml.safe_load(f)

with ThreadPoolExecutor(max_workers=2) as executor:
    future_list = []
    for device in devices:
        future = executor.submit(send_show, device, 'sh clock')
        future_list.append(future)
    # то же самое в виде list comprehensions:
    # future_list = [executor.submit(send_show, device, 'sh clock') for device in devices]
    for f in as_completed(future_list):
        print(f.result()) # если использовать функцию as_completed - можно получать результаты по мере того как функции завершают работу


