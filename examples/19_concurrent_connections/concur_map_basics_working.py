import netmiko
from pprint import pprint
import yaml
import logging
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

'''
Basic example : connection one-by-one, w/o concurrent
'''
# def send_show (device,commands):
#     result={}
#     try:
#         with netmiko.ConnectHandler(**device) as ssh:  # Подключение по SSH, '**' значит распаковать словарь в ключевые аргументы
#             ssh.enable()
#             for comm in commands:
#                 output=ssh.send_command(comm)
#                 result[comm]=output
#             return result
#     except (netmiko.NetmikoTimeoutException, netmiko.NetmikoAuthenticationException) as error:
#         print(error)
#
#
#
# if __name__ == "__main__":
#     with open("devices.yaml") as f: # словарь, записанный в файл, определяющий параметры устройств
#         devices = yaml.safe_load(f)
#     for device in devices:
#         result = send_show(device, ["sh clock", "sh ip int br"])
#         pprint(result)



'''
Basic up-level : 
- logging module application
'''

# logging.getLogger('netmiko').setLevel(logging.INFO)
# logging.basicConfig(
#     format = '%(asctime)s %(threadName)s %(levelname)s: %(message)s',
#     level=logging.INFO)
#
# def send_show (device,commands):
#     start_msg='=> Connection : {}'
#     received_msg='<= Received : {}'
#     host=device['host']
#     logging.info(start_msg.format(host))
#     result={}
#     try:
#         with netmiko.ConnectHandler(**device) as ssh:  # Подключение по SSH, '**' значит распаковать словарь в ключевые аргументы
#             ssh.enable()
#             for comm in commands:
#                 output=ssh.send_command(comm)
#                 result[comm]=output
#                 logging.info(received_msg.format(host))
#             return result
#     except (netmiko.NetmikoTimeoutException, netmiko.NetmikoAuthenticationException) as error:
#         logging.warning(f'Alert : {error}')
#
#
#
# if __name__ == "__main__":
#     with open("devices.yaml") as f: # словарь, записанный в файл, определяющий параметры устройств
#         devices = yaml.safe_load(f)
#     for device in devices:
#         result = send_show(device, ["sh clock", "sh ip int br"])
#         pprint(result)

'''
Basic up-level : 
- logging module application
- concurrent connection
'''

logging.getLogger('netmiko').setLevel(logging.INFO)
logging.basicConfig(
    format = '%(asctime)s %(threadName)s %(levelname)s: %(message)s',
    level=logging.INFO)

def send_show (device,commands):
    start_msg='=> Connection : {}'
    received_msg='<= Received : {}'
    host=device['host']
    logging.info(start_msg.format(host))
    result={}
    try:
        with netmiko.ConnectHandler(**device) as ssh:  # Подключение по SSH, '**' значит распаковать словарь в ключевые аргументы
            ssh.enable()
            for comm in commands:
                output=ssh.send_command(comm)
                result[comm]=output
                logging.info(received_msg.format(host))
            return result
    except (netmiko.NetmikoTimeoutException, netmiko.NetmikoAuthenticationException,netmiko.exceptions.ReadTimeout) as error:
        logging.warning(f'ALERT  : {error}')


def collect_data(device,command,max_threads=2):
    fin_data={}
    with ThreadPoolExecutor (max_workers=max_threads) as ex:
        execution_result = ex.map(send_show,devices,repeat(command))
        for dev, output in zip(device,execution_result):
            fin_data[dev['host']]=output
    return fin_data

if __name__ == "__main__":
    with open("devices.yaml") as f: # словарь, записанный в файл, определяющий параметры устройств
        devices = yaml.safe_load(f)
    pprint(collect_data(devices,'sh clock'))

