from . import BaseProtocol
from urllib.request import urlopen

class FTPProtocol(BaseProtocol):
    def __init__(self):
        pass

    def download(self, url, target, chunk_size):
        response = urlopen(url)
        with open(target, 'wb') as f:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
