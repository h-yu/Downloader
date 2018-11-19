import download
import tempfile
import shutil

class TestDownloader:
    def setup(self):
        print("setup")
        self.target_dir = tempfile.mkdtemp()
        self.input_path = self.target_dir + "/input"
        with open(self.input_path, 'a') as the_file:
            the_file.write('http://URL1\nhttp://URL1\nftp://URL2\n')

    def teardown(self):
        print("teardown")
        shutil.rmtree(self.target_dir)

    def test_init(self, capsys):
        d = download.Downloader(self.target_dir, self.input_path, 1024)
        assert len(d.lineset) == 2

    def test_protocol_from_url(self):
        protocol = download.Downloader.protocol_from_url(None, "http://asdf")
        assert protocol == "http"
        protocol = download.Downloader.protocol_from_url(None, "://asdf")
        assert protocol is None
        protocol = download.Downloader.protocol_from_url(None, "blah")
        assert protocol is None
