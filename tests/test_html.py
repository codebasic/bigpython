# coding: utf-8
import os

from bigpython import webscrap
from bigpython.webscrap  import http, html

def test_extract_table():
    url = 'https://ko.wikipedia.org/wiki/%EC%95%A8%EB%9F%B0_%ED%8A%9C%EB%A7%81'
    filename = http.download(url, 'turing_wiki.html')
    with open(filename) as f:
        html_doc = html.Html(f)
    # 파일 삭제
    os.unlink(filename)

    table_frame = html_doc.extract_tables('table.wikitable')
    assert table_frame[0].ix[0,0] == '1912년'

def test_get_html():
    # source is url
    url = 'https://ko.wikipedia.org/wiki/%EC%95%A8%EB%9F%B0_%ED%8A%9C%EB%A7%81'
    html_doc = webscrap.get_html(url)
    assert html_doc.title.text == "앨런 튜링 - 위키백과, 우리 모두의 백과사전"

    # source is file
    filename = http.download(url, 'turing_wiki.html')
    html_doc = webscrap.get_html(filename)

    assert html_doc.title.text == "앨런 튜링 - 위키백과, 우리 모두의 백과사전"

    # cleanup
    os.unlink(filename)
