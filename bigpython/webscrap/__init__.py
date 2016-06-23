# coding: utf-8
import pip
import platform, sys, os, stat, zipfile
import time
from urllib.parse import urlparse
import re

import requests

from . import html, http

def get_html(src, encoding='utf-8'):
    """Returns BeautifulSoup from URL or file

    src: url or filepath
    encoding: (default=utf-8)
    """
    # check if url or filepath
    scheme = urlparse(src).scheme
    if re.compile('(http|https)').match(scheme):
        res = requests.get(src)
        doc = res.text
    else:
        doc = open(src, encoding=encoding)

    # select parser for BeautifulSoup
    # return BeautifulSoup(doc, parser)
    return html.Html(doc)

def get_browser(browser='Chrome', driverpath=None):
    driver_map = {'Chrome': 'chromedriver'}

    try:
        from selenium import webdriver
    except ImportError:
        setup_webdriver()
        try:
            from selenium import webdriver
        except:
            raise
    else:
        if driverpath is None:
            driverpath = os.path.join('.', driver_map[browser])
        driver = getattr(webdriver, browser)(driverpath)
        return driver


def setup_webdriver():
    # selenium package 설치
    pip.main(['install', 'selenium'])

    print('chromedriver 다운로드')
    downloaded_file = download_chromedriver()
    print(downloaded_file)

    # 압축 해제
    print('다운로드 받은 파일 압축 해제 ...')
    driverzip = zipfile.ZipFile(downloaded_file)
    driverzip.extractall()
    driverfile = driverzip.namelist()[0]
    driverzip.close()

    # 실행권한 설정
    st = os.stat(driverfile)
    os.chmod(driverfile, st.st_mode | stat.S_IEXEC)

    print('설정 테스트 ...', end=' ')
    test_webdriver(driverfile)
    print('완료')

def download_chromedriver():
    driverfile_map = {'Windows': 'chromedriver_win32.zip',
        'Darwin': 'chromedriver_mac32.zip'}
    download_target = driverfile_map.get(platform.system(), None)
    if download_target is None:
        sys.exit('No chromedriver for {0}'.format(platform.system()))

    chromedriver_url = 'http://chromedriver.storage.googleapis.com/2.22/'
    chromedriver_url = chromedriver_url + download_target

    driverfilepath = http_download(chromedriver_url, download_target)
    return driverfilepath

def test_webdriver(driverfile):
    from selenium import webdriver
    chrome = webdriver.Chrome(os.path.join('.',driverfile))
    chrome.get('http://www.gogle.com')
    time.sleep(5)
    search_box = chrome.find_element_by_name('q')
    search_box.send_keys('파이썬')
    time.sleep(5)
    search_box.submit()
    time.sleep(10)
    chrome.quit()

if __name__ == '__main__':
    setup_webdriver()
