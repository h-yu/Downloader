from . import BaseProtocol
import paramiko
import shutil
import urllib

class SFTPProtocol(BaseProtocol):
    def __init__(self):
        pass

    def download(self, url, target, chunk_size):
        parsed = urllib.parse.urlparse(url)
        user = parsed.username
        password = parsed.password
        host = parsed.hostname
        host_path = parsed.path
        ssh =paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=password, look_for_keys=False)
        sftp = ssh.open_sftp()
        sftp_file = sftp.open(host_path, bufsize=chunk_size)
        shutil.copyfileobj(sftp_file, open(target, 'wb', chunk_size), chunk_size)
