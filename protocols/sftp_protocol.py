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
        print("user: " + user)
        print("password: " + password)
        print("host: " + host)
        print("host_path: |" + host_path + "|")
        print("target: " + target)
        """
        user = "demo"
        password = "password"
        host = "test.rebex.net:22"
        """
        ssh =paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=password, look_for_keys=False)
        sftp = ssh.open_sftp()
        print("ABCD1")
        sftp_file = sftp.open(host_path, bufsize=chunk_size)
        print("ABCD2")
        shutil.copyfileobj(sftp_file, open(target, 'wb', chunk_size), chunk_size)
        print("ABCD3")


        """
        #sftp://demo:password@test.rebex.net:22/pub/example/readme.txt
        sftp demo@test.rebex.net:/pub/example/readme.txt ./readme.txt
        host = "test.rebex.net:22"
        port = 22
        transport = paramiko.Transport((host, port))

        username = "demo"
        password = "password"
        transport.connect(username = username, password = password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        import sys
        path = '/pub/example/readme.txt'
        localpath = target
        sftp_file = sftp.open(localpath, path)

        sftp.close()
        transport.close()
        print 'Upload done.'
        """