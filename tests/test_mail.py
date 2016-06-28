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
def mailclient(request):
    host = getattr(request.module, 'host', 'naver.com')
    mailclient = EmailClient(host)
    mailclient.login(configfile=get_config())
    return mailclient

def test_create_emailclient():
    assert EmailClient('naver.com') != None

def test_login():
    host = 'naver.com'
    mailclient = EmailClient(host)
    assert mailclient.login(configfile=get_config())

def test_search(mailclient):
    message_ids = mailclient.search(['SUBJECT', '빅파이'])
    for header in mailclient.get_subjects(message_ids):
        assert '빅파이' in header['Subject']

def test_get_text(mailclient):
    message_ids = mailclient.search(['SUBJECT', '빅파이'])
    for mid in message_ids:
        for content_type, text in mailclient.get_text(mid):
            assert content_type.startswith('text')

def test_download_attachments(mailclient):
    message_ids = mailclient.search(['SUBJECT', '빅파이'])

    download_files = []

    for mid in message_ids:
        attachment_list = mailclient.download_attachments(mid)
        for filepath in attachment_list:
            assert os.path.exists(filepath)
            download_files.append(filepath)

    for mid in message_ids:
        userhome = os.path.expanduser('~')
        target_dir = os.path.join(userhome, 'Downloads')
        attachment_list = mailclient.download_attachments(mid, target_dir=target_dir)
        for filepath in attachment_list:
            assert os.path.exists(filepath)
            download_files.append(filepath)

    for filepath in download_files:
        os.unlink(filepath)


def test_sendmail(mailclient):
    msg = 'Subject: I am seongjoo\nThank you.'
    result = mailclient.send_message('seongjoo@codebasic.co', msg)
    assert not result
