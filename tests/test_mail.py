import os

from bigpython.mail import EmailClient

def test_create_emailclient():
    mail = EmailClient('imap.naver.com', ssl=True)
    configfile = 'login.cfg'
    configfile = os.path.join(os.path.dirname(__file__), configfile)
    if not os.path.exists(configfile):
        raise FileNotFoundError('로그인 설정 파일 경로 문제: {}'.format(
            os.path.abspath(configfile)))
    mail.login(configfile=configfile)
