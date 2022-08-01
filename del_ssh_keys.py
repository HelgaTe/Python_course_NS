import re
import subprocess

regex = r"^(\d+.){3}\d+.*$"
ssh_file = "/Users/Olha/.ssh/known_hosts"


def del_ssh_key(file):
    """
    Delete ssh keys
    :param file: SSH key file
    @return: result
    """
    with open(file) as f:
        content = f.read()
        content_lines = content.splitlines()
        new_content = ""
        for line in content_lines:
            result = re.search(regex, line)
            if result:
                pass
            else:
                new_content += line + "\n"
    with open(file, "w") as f2:
        f2.write(new_content)


def run(cmd=None, directory="", raw=False):
    """
    Run command
    :param cmd: command
    :param directory: base directory
    :param raw: if raw mode used, subprocess object returned, if not stdout
    :return: stdout of the command or subprocess object
    """
    if not directory:
        result = subprocess.run(
            cmd,
            cwd=f"./{directory}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encodin="utf-8",
        )
    else:
        result = subprocess.run(
            cmd,
            cwd=f"{directory}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encodin="utf-8",
        )
        output = result.stdout
        if raw:
            return result
        return output.strip()


def add_new_ssh_keys(ip_list):
    """
    Add new keys for IP addresses in the list
    @param ip_list: list of IP addresses of devices
    @return:
    """
    for ip in ip_list:
        result = subprocess.run(f'ssh cisco@{ip}', shell=True, capture_output=True, text=True, input="yes")
        print(result)


del_ssh_key(ssh_file)
add_new_ssh_keys(['172.16.100.129', '172.16.100.130', '172.16.100.131'])
