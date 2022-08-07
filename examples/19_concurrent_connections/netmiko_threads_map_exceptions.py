import logging
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import repeat
from pprint import pprint

import yaml
from netmiko import ConnectHandler, NetMikoAuthenticationException

logging.getLogger('paramiko').setLevel(logging.WARNING) # name of the module that creates a log + logging level

logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

# При использовании метода map, обработку исключений лучше делать внутри функции, которая запускается в потоках
def send_show(device_dict, command):
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device_dict['host']
    logging.info(start_msg.format(datetime.now().time(), ip))
    if ip == '172.16.100.129': time.sleep(5)

    try:
        with ConnectHandler(**device_dict) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
            logging.info(received_msg.format(datetime.now().time(), ip))
        return result
    # except NetMikoAuthenticationException as err: # initial version
    #     logging.warning(err)
    except Exception as err: # modified version
        logging.warning(f'{ip} failed', err)



def send_command_to_devices(devices, command):
    data = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        result = executor.map(send_show, devices, repeat(command))
        for device, output in zip(devices, result):
            data[device['host']] = output
    return data


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
    pprint(send_command_to_devices(devices, 'sh ip int br'))

