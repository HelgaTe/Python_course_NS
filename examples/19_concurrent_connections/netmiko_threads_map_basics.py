import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import repeat

import netmiko
import yaml

logging.getLogger('paramiko').setLevel(logging.WARNING)

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def send_show(device, show):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device['host']
    logging.info(start_msg.format(datetime.now().time(), ip))
    if ip == '172.16.100.129': # при подключении к 172.16.100.1xx сделать паузу на xx сек==> маршрутизатор с этим адресом будет отрабатывать дольше
        time.sleep(10)

    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(show)
        logging.info(received_msg.format(datetime.now().time(), ip))
        return result


with open('devices.yaml') as f:
    devices = yaml.safe_load(f)

with ThreadPoolExecutor(max_workers=3) as executor: # класс ThreadPoolExecutor инициируется в блоке with с указанием количества потоков
    result = executor.map(send_show, devices, repeat('sh clock'))
    for device, output in zip(devices, result):
        print(device['host'], output)
