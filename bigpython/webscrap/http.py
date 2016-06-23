# coding: utf-8
import sys
import os
from urllib.parse import urlparse, unquote, unquote_plus

import requests

def download(url, filepath, chunksize=100000):
    res = requests.get(url)
    res.raise_for_status()
    if os.path.exists(filepath):
        print('File already exists')
        return filepath

    with open(filepath, 'wb') as f:
        for chunk in res.iter_content(chunksize):
            f.write(chunk)

    return filepath

def unquote_url(url):
    if '+' in url:
        return unquote_plus(url)
    return unquote(url)
