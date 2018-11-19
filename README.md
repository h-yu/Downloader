# Downloader

Downloader accepts a list of URLs and a target path. It downloads from those URLs to the target path in parallel. Downloader supports the http and ftp protocols and is extensible to support additional ones if needed.

### Prerequisites

Python 3

pip

pytest

requests

### Installing

Install python 3. Install pip.

Run the following in the project root directory:

```
pip install -r requirements.txt
```
You must run this before running the program or it may not work properly.

### Running the program
```
$ python download.py -h
usage: download.py [-h] [-t TARGET] [-i INPUT] [-c CHUNK_SIZE]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        target download location
  -i INPUT, --input INPUT
                        input url list
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        chunk size for streaming downloads
```
Downloader requires as input a line-separated list of URLs to download, and a path to save the files.
If the target directory does not exist, one will be created.

## Running the tests

Downloader uses pytest for unit and integration tests. Run them with the following command:
```
pytest
```

### Test Breakdown

test_protocols.py contains integration tests for the supported protocols.

An internet connection is required to run these tests as they download from remote sources.

test_downloader.py contains unit tests for Downloader.

Currently it tests the input validation methods as well as protocol extraction from URLs.

## Built With

* [Requests](http://docs.python-requests.org/en/master/) - Library for http requests
* [pytest](https://docs.pytest.org/en/latest/contents.html) - Test framework
* [python 3](https://www.python.org/downloads/)
