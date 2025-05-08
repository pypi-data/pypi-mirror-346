
import paramiko
import time
from aicastle.deepracer.vehicle.api import vehicle_control_module_content

class RebootTrigger:
    def __init__(self, ssh_client, password, reboot_seconds=20):
        self.ssh_client = ssh_client
        self.password = password
        self.rebooted = False
        self.reboot_seconds = reboot_seconds

    def run(self):
        print("Rebooting...")
        stdin, stdout, stderr = ssh_sudo_command(self.ssh_client,  "reboot", self.password)    
        time.sleep(self.reboot_seconds)
        self.rebooted = True

def ssh_connect(hostname, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)

    return ssh_client

def ssh_sudo_command(ssh_client, command, password):
    sudo_command = f"sudo -S -p '' {command}"
    stdin, stdout, stderr = ssh_client.exec_command(sudo_command, get_pty=True)
    time.sleep(1)
    stdin.write(password + "\n")
    stdin.flush()
    return stdin, stdout, stderr

def ssh_remote_content_update(hostname, username, password, remote_file_path, new_content):
    # ssh 연결
    ssh_client = ssh_connect(hostname=hostname, username=username, password=password)
    # 파일 권한 수정
    stdin, stdout, stderr = ssh_sudo_command(ssh_client, f"chmod o+w {remote_file_path}", password)
    # 원격 파일 읽기
    with ssh_client.open_sftp().open(remote_file_path, 'r') as remote_file:
        remote_content = remote_file.read().decode('utf-8')
    
    # 파일 수정할 필요가 없으면 종료
    if remote_content == new_content:
        ssh_client.close()
        reboot_trigger = None
        return reboot_trigger
    # 파일 수정
    else:
        sftp_client = ssh_client.open_sftp()
        with sftp_client.open(remote_file_path, 'w') as remote_file:
            remote_file.write(new_content)

        reboot_trigger = RebootTrigger(ssh_client, password)
        return reboot_trigger

def vehicle_control_module_content_update(hostname, username, password, custom=True):
    remote_file_path="/opt/aws/deepracer/lib/webserver_pkg/lib/python3.8/site-packages/webserver_pkg/vehicle_control.py"
    if custom:
        new_content = vehicle_control_module_content.custom_content
    else:
        new_content = vehicle_control_module_content.origin_content

    reboot_trigger =  ssh_remote_content_update(hostname, username, password, remote_file_path, new_content)
    return reboot_trigger

