import pexpect
from getpass import getpass
from pprint import pprint

def send_show_command (ip, user, passwd, command):
    print(f'Trying to connect to {ip}')
    cmd_output_dict={}
    try:
        with pexpect.spawn (f'ssh {user}@{ip}',timeout=10,encoding='utf-8') as ssh:
            ssh.expect('Password')

            ssh.sendline(passwd)
            ssh.expect(['>','#'])

            ssh.sendline('terminal length 0')
            ssh.expect(['>','#'])

            if type(command)==str:
                command = [command]
            for cmd in command:
                ssh.sendline(cmd)
                ssh.expect('>')
                output=ssh.before + ssh.after # to catch '>' in R name
                output=output.replace('\r\n','\n')
                cmd_output_dict[cmd]=output
            return cmd_output_dict
    except pexpect.TIMEOUT as error:
        print(f'Error - connection failed')

if __name__ == "__main__":

    ip_list=['172.16.100.129', '172.16.100.130', '172.16.100.131','176.16.100.132']
    command=['show clock','show ip interface brief']
    user=input('Username : ')
    passwd=getpass()

    result={}

    for ip in ip_list:
        out=send_show_command(ip, user, passwd,command)
        result[ip]=out
        pprint(result)