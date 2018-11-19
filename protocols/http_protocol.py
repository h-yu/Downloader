from . import BaseProtocol
import requests



class HTTPProtocol(BaseProtocol):
    def __init__(self):
        pass

    def download(self, url, target, chunk_size):
        r = requests.get(url, stream=True)
        with open(target, "wb") as file:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)

