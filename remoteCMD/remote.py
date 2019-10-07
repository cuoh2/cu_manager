import os
import paramiko

from manager.models import HostInfo


class Remote:
    def __init__(self, host, username, password, port=22):
        self.host=host
        self.usename=username
        self.password=password
        self.port=port

    def ssh(self, cmd):
        self.cmd=cmd
        try:
            transport=paramiko.Transport((self.host, self.port))
            transport.connect(username=self.usename, password=self.password)
        except Exception as e:
            raise e
        else:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh._transport = transport
            stdin, stdout, stderr = ssh.exec_command(self.cmd)
            result=stdout.readlines()
            transport.close()
            return result

class SFtp(Remote):
    def ssh(self,cmd=''):
        try:
            self.transport = paramiko.Transport((self.host, self.port))
            self.transport.connect(username=self.usename, password=self.password)
        except Exception as e:
            return False
        else:
            return True

    def put(self,upload_file, remote_path='/home/tmp/'):
        if self.ssh():
            self.upload_file = upload_file.replace('\\', '/')
            self.remote_path = remote_path + os.path.split(self.upload_file)[-1]
            sftp=paramiko.SFTPClient.from_transport(self.transport)
            sftp.put(self.upload_file, self.remote_path)
            self.transport.close()

    def get(self, getfile, savepath):
        self.getfile = getfile
        self.savepath = savepath
        if self.ssh():
            sftp=paramiko.SFTPClient.from_transport(self.transport)
            sftp.get(self.getfile, self.savepath)
            self.transport.close()


def get_host_info(ip, admin, password, nickname):
    try:
        r = Remote(host=ip,username=admin,password=password)
        host = HostInfo()
        host.ip = ip
        host.host_name = nickname
        host.cpu = str(r.ssh('cat /proc/cpuinfo | grep name |cut -f2 -d:')[0].replace('\n', ''))# cpu信息
        host.os=str(r.ssh('cat /etc/issue')[0].replace('\\n', '').replace('\\l\n', ''))# 系统版本
        host.last_login_time=str(r.ssh("who -b | cut -d ' ' -f 13,14")[0].replace('\n', ''))# 上次登录时间
        host.is_delete=False
        host.save()
        return True
    except Exception as e:
        raise e

