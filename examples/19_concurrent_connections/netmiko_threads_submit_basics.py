import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

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
        # print(future_list) # future shows execution status
    for f in future_list:
        print(f.result()) # результаты возвращаются в порядке создания Future; если использовать функцию as_completed - можно получать результаты по мере того как функции завершают работу
        # print(future_list)

