import argparse
import utils
import protocols
import os
import multiprocessing
import time

class Downloader:
    def __init__(self, target, input_list, chunk_size, max_retries=3, retry_sleep=1):
        self.target = self.process_target(target)
        self.input_list = input_list
        self.chunk_size = chunk_size
        self.max_retries = max(max_retries, 1)
        self.retry_sleep= max(retry_sleep, 0)
        with open(input_list) as f:
            lines = f.read().splitlines()
            self.lineset = self.process_input_list(lines)

    def process_target(self, target_str):
        if len(target_str) == 0 or target_str[-1] != "/":
            target_str += "/"
        if not os.path.exists(target_str):
            os.makedirs(target_str)
        return target_str

    def process_input_list(self, input_list):
        lineset = set()
        for item in input_list:
            item = item.strip()
            if utils.protocol_from_url(item):
                lineset.add(item)
        return lineset

    def run_one_download(self, protocol, url, target_file, chunk_size):
        for i in range(self.max_retries):
            try:
                protocol.download(url, target_file, chunk_size)
            except Exception as e:
                print("Downloading from {} failed because of error: {}".format(url, e))
                # If an exception was raised (e.g. connection was lost),
                # remove any partial data that was downloaded.
                if os.path.exists(target_file):
                    os.remove(target_file)
                time.sleep(self.retry_sleep)
            else:
                break


    def get_protocol(self, url):
        try:
            protocol_id = utils.protocol_from_url(url)
            protocol = protocols.grab(protocol_id)
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
            download_path = self.target + utils.filename_from_url(url)
            if not os.path.exists(download_path):
                print("Downloading with filename {} from {}".format(utils.filename_from_url(url), url))
                proc = multiprocessing.Process(target=self.run_one_download, args=(protocol, url, self.target + utils.filename_from_url(url), self.chunk_size,))
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
