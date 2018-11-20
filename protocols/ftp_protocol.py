from . import BaseProtocol
import urllib.request

class FTPProtocol(BaseProtocol):
    def __init__(self):
        pass

    def download(self, url, target, chunk_size):
        response = urllib.request.urlopen(url)
        with open(target, 'wb') as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
