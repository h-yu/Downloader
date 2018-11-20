import download
import tempfile
import shutil
import protocols
import os
from tests.mocked_connection import MockConnection
from unittest import mock

def mocked_get(*args, **kwargs):
    if args[0].endswith('FAIL'):
        return MockConnection("ABCD1234", fail_on=2)
    return MockConnection("ABCD1234")

class TestDownloader:
    def setup(self):
        print("setup")
        self.get_count = 0
        self.target_dir = tempfile.mkdtemp()
        self.input_path = self.target_dir + "/input"
        with open(self.input_path, 'a') as the_file:
            the_file.write('http://URL1\nhttp://FAIL\nftp://URL2\nhttp://URL1\n')


    def teardown(self):
        print("teardown")
        shutil.rmtree(self.target_dir)

    # Test that the downloader creates a set of unique URLs
    # Test that if a download fails, the others still succeed
    @mock.patch('requests.get', side_effect=mocked_get)
    @mock.patch('urllib.request.urlopen', side_effect=mocked_get)
    def test_downloads(self, ftpget, httpget):
        d = download.Downloader(self.target_dir, self.input_path, 1)
        assert len(d.lineset) == 3
        d.run_downloads()
        files = os.listdir(self.target_dir)
        assert len(files) == 3
        with open(self.target_dir + "/5WRuQtcrULW95wE5KWCZrw", 'r') as myfile:
            data = myfile.read()
            assert data == "ABCD1234"
        with open(self.target_dir + "/MI2FWyO3Voqg0BAJutfTxg", 'r') as myfile:
            data = myfile.read()
            assert data == "ABCD1234"

    # Test that the downloader retries when an exception is thrown during download (i.e. connection lost)
    @mock.patch('requests.get', side_effect=mocked_get)
    def test_retries(self, httpget, capsys):
        d = download.Downloader(self.target_dir, self.input_path, 1)
        http_protocol = protocols.grab('http')
        d.run_one_download(http_protocol, 'http://FAIL', self.target_dir + "/test", 1)
        captured = capsys.readouterr()
        with open('./loool', 'wb') as myfile:
            myfile.write(str(captured).encode())
        assert captured.out == "setup\nDownloading from http://FAIL failed because of error: \nDownloading from http://FAIL failed because of error: \nDownloading from http://FAIL failed because of error: \n"
