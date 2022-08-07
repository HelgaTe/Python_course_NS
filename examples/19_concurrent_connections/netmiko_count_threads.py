from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoAuthenticationException


def send_show(device_dict, commands): # последовательное подключение
    if type(commands) == str:
        commands = [commands]
    ip = device_dict['host']
    result = ''
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        for command in commands:
            result += ssh.send_command(command) # записать вывод переданных команд в список
    return {ip: result}


def send_command_to_devices(devices, commands, max_threads=2): # параллельное поделючение потоками
    data = {}
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_ssh = [
            executor.submit(send_show, device, commands) for device in devices
        ]
        for f in as_completed(future_ssh):
            result = f.result()
            data.update(result)
    return data


if __name__ == '__main__':
    filename = 'devices_all.yaml'
    min_th, max_th = 3, 9

    with open(filename) as f:
        devices = yaml.safe_load(f)
        # pprint(send_command_to_devices(devices,['sh clock','sh ip interface'],max_threads=3)) # протестировать выполнение параллельного подключения
        # for dev in devices: # строки - чтобы протестировать работу функции на списке команд
        #     pprint(send_show(dev,['sh clock','sh ip interface']))
    print('Количество устройств:', len(devices))



    for num_threads in range(min_th, max_th+1):
        print(' {} потоков '.format(num_threads).center(50, '#'))
        start_time = datetime.now()
        all_done = send_command_to_devices(devices, commands='sh ip int br', max_threads=num_threads)
        print(datetime.now() - start_time)

