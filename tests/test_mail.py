# coding: utf-8
import os

import pytest
from bigpython.mail import EmailClient

def get_config(configfile='login.cfg'):
    configfile = os.path.join(os.path.dirname(__file__), configfile)
    if not os.path.exists(configfile):
        raise FileNotFoundError('로그인 설정 파일 경로 문제: {}'.format(
            os.path.abspath(configfile)))
    return configfile

@pytest.fixture(scope='module')
def imapclient(request):
    host = getattr(request.module, 'host', 'imap.naver.com')
    imapclient = EmailClient(host, ssl=True)
    imapclient.login(configfile=get_config())
    return imapclient

def test_create_emailclient():
    assert EmailClient('imap.naver.com', ssl=True) != None

def test_login():
    host = 'imap.naver.com'
    imapclient = EmailClient(host, ssl=True)
    assert imapclient.login(configfile=get_config())

def test_search(imapclient):
    message_ids = imapclient.search(['SUBJECT', '빅파이'])
    for header in imapclient.get_subjects(message_ids):
        assert '빅파이' in header['Subject']
