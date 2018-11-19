import protocols
import os
import tempfile
import shutil

class TestProtocols:
    def setup(self):
        print("setup")
        self.target_dir = tempfile.mkdtemp()

    def teardown(self):
        print("teardown")
        shutil.rmtree(self.target_dir)

    def test_http(self, capsys):
        http_instance = protocols.grab('http_protocol')
        target_path = self.target_dir + "/agoda-logo.svg"

        http_instance.download("http://cdn6.agoda.net/images/mvc/default/agoda-logo.svg", target_path, 1024)
        assert os.path.exists(target_path)

    def test_ftp(self, capsys):
        ftp_instance = protocols.grab('ftp_protocol')
        target_path = self.target_dir + "/test.zip"

        ftp_instance.download("ftp://speedtest.tele2.net/512KB.zip", target_path, 1024)
        assert os.path.exists(target_path)
