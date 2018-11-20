import protocols
import os
import tempfile
import shutil
from tests.mocked_connection import MockConnection
from unittest import mock

def mocked_get(*args, **kwargs):
    if args[0] == 'http://www.download.com/connection-lost.txt':
        return MockConnection("ABCD1234", fail_on=2)
    return MockConnection("ABCD1234")

class TestProtocols:
    def setup(self):
        print("setup")
        self.target_dir = tempfile.mkdtemp()

    def teardown(self):
        print("teardown")
        shutil.rmtree(self.target_dir)

    @mock.patch('requests.get', side_effect=mocked_get)
    def test_http(self, capsys):
        http_instance = protocols.grab('http_protocol')
        target_path = self.target_dir + "/test_http.txt"
        target_path2 = self.target_dir + "/test_http2.txt"

        http_instance.download("http://www.download.com/success.txt", target_path, 1024)
        assert os.path.exists(target_path)
        with open(target_path, 'r') as myfile:
            data = myfile.read()
            assert data == "ABCD1234"

        thrown = False
        try:
            http_instance.download("http://www.download.com/connection-lost.txt", target_path2, 1)
        except:
            thrown = True
        assert thrown


    @mock.patch('urllib.request.urlopen', side_effect=mocked_get)
    def test_ftp(self, capsys):
        ftp_instance = protocols.grab('ftp_protocol')
        target_path = self.target_dir + "/test_ftp.txt"
        target_path2 = self.target_dir + "/test_ftp2.txt"

        ftp_instance.download("http://www.download.com/success.txt", target_path, 1024)
        assert os.path.exists(target_path)

        thrown = False
        try:
            ftp_instance.download("http://www.download.com/connection-lost.txt", target_path2, 1)
        except:
            thrown = True
        assert thrown


    def test_sftp(self, capsys):
        with mock.patch('paramiko.SSHClient') as MockSFTP:
            MockSFTP.return_value.open_sftp.return_value.open.return_value = MockConnection("ABCD1234")
            sftp_instance = protocols.grab('sftp')
            target_path = self.target_dir + "/test_sftp.txt"
            target_path2 = self.target_dir + "/test_sftp2.txt"

            sftp_instance.download("sftp://user:pass@www.download.com/success.txt", target_path, 1024)
            assert os.path.exists(target_path)

            MockSFTP.return_value.open_sftp.return_value.open.return_value = MockConnection("ABCD1234", fail_on=2)
            thrown = False
            try:
                sftp_instance.download("sftp://user:pass@www.download.com/failure.txt", target_path2, 2)
            except:
                thrown = True
            assert thrown

    def test_grab(self, capsys):
        http_instance = protocols.grab('http')
        assert http_instance is not None
        http_instance = protocols.grab('http_protocol')
        assert http_instance is not None
        sftp_instance = protocols.grab('sftp')
        assert sftp_instance is not None
        ftp_instance = protocols.grab('ftp')
        assert ftp_instance is not None
        thrown = False
        try:
            protocols.grab('fake')
        except ImportError:
            thrown = True
        assert thrown
