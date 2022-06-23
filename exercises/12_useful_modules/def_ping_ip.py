import subprocess


def ping_ip(ip):

    result = subprocess.run(
        ['ping', '-c', '3', '-n', ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if result.returncode == 0:
        return True
    else:
        return False


if __name__ == '__main__':

    ip_list = ['192.168.1.3', '8.8.8.8', '8.8.8.5', 'test']
    for ip in ip_list:
        status = ping_ip(ip)
        if status:
            print(f'Адрес {ip} пингуется')
        else:
            print(f'Адрес {ip} не пингуется')
