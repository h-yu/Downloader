import json
import argparse
import protocols
import uuid,base64
import re
import os
import multiprocessing

class Downloader:
    def __init__(self, target, input_list, chunk_size):
        self.target = self.process_target(target)
        self.input_list = input_list
        self.chunk_size = chunk_size
        with open(input_list) as f:
            lines = f.read().splitlines()
            self.lineset = self.process_input_list(lines)

    def process_target(self, target_str):
        if len(target_str) == 0 or target_str[-1] != "/":
            target_str += "/"
        if not os.path.exists(target_str):
            os.makedirs(target_str)
        return target_str

    def protocol_from_url(self, url):
        """
        Given a url, extracts the protocol acronym
        """
        #pattern = re.compile("^[^:]+(?=:\/\/)")
        pattern = re.compile("^[^:]+(?=://)")
        match = pattern.search(url)
        if match:
            return match.group(0)

    def process_input_list(self, input_list):
        lineset = set()
        for item in input_list:
            item = item.strip()
            if self.protocol_from_url(item):
                lineset.add(item)
        return lineset

    def filename_from_url(self, url):
        """
        Creates a unique filename based on the URL. There is a vanishingly small
        chance of filename collision, but I've left the function this way because
        I feel it's worth it to have shorter filenames. Collisions could be
        completely avoided by something like just base64 encoding the url
        """
        name = str(uuid.uuid5(uuid.NAMESPACE_DNS, url))
        short = base64.encodebytes(uuid.UUID(name).bytes).decode("ascii").rstrip('=\n').replace('/', '_')
        return short

    def run_one_download(self, protocol, url, target_file, chunk_size):
        try:
            protocol.download(url, target_file, chunk_size)
        except Exception as e:
            print("Skipped downloading from {} because of error: {}".format(url, e))
            if os.path.exists(target_file):
                os.remove(target_file)

    def get_protocol(self, url):
        try:
            protocol_id = self.protocol_from_url(url)
            protocol = protocols.grab(protocol_id + "_protocol")
            return protocol
        except ImportError as e:
            print("Could not get protocol for {} because {}".format(url, e))
        return None

    def run_downloads(self):
        procs = []
        for url in self.lineset:
            protocol = self.get_protocol(url)
            if not protocol:
                continue
            download_path = self.target + self.filename_from_url(url)
            if not os.path.exists(download_path):
                print("Downloading to {} from {}".format(self.target + self.filename_from_url(url), url))
                proc = multiprocessing.Process(target=self.run_one_download, args=(protocol, url, self.target + self.filename_from_url(url), self.chunk_size,))
                procs.append(proc)
                proc.start()
            else:
                print("Skipped {} because the file already exists on disk".format(url))

        for proc in procs:
            proc.join()
        print("Finished.")

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", type=str, required=True,
                        help="target download location")
    parser.add_argument("-i", "--input", type=str, required=True,
                        help="input url list")
    parser.add_argument("-c", "--chunk-size", type=int, default=1024,
                        help="chunk size for streaming downloads")
    args = parser.parse_args()


    try:
        d = Downloader(args.target, args.input, args.chunk_size)
    except NotADirectoryError as e:
        print("Target path {} exists but is not a directory. Exiting.".format(args.target))
        quit()
    except Exception as e:
        print("Exiting because of error: {}".format(e))
        quit()

    d.run_downloads()


if __name__ == '__main__':
    main()
