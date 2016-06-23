# coding: utf-8
import pytest
import requests
import os
from urllib.parse import quote_plus

from bigpython.webscrap import http

def test_unquote_url():
    url = 'https://ko.wikipedia.org/wiki/%EC%95%A8%EB%9F%B0_%ED%8A%9C%EB%A7%81'
    url_unquoted = http.unquote_url(url)
    basename = os.path.basename(url_unquoted)
    assert basename == '앨런_튜링'

    url_quote_plus = quote_plus(url_unquoted)
    url_unquoted = http.unquote_url(url_quote_plus)
    basename = os.path.basename(url_unquoted)
    assert basename == '앨런_튜링'

def test_http_download():
    url = 'https://ko.wikipedia.org/wiki/%EC%95%A8%EB%9F%B0_%ED%8A%9C%EB%A7%81'
    filename = http.download(url, '앨런튜링_위키.html')
    assert os.path.exists(filename)
    # cleanup
    os.unlink(filename)

    with pytest.raises(requests.ConnectionError):
        http.download('http://no-such-domain.com', 'no.html')

    with pytest.raises(requests.HTTPError):
        http.download('http://google.com/404', 'no.html')
