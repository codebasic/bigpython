# coding: utf-8
import os
import configparser
import email
from email.header import decode_header
import subprocess
import getpass

from imapclient import IMAPClient

class EmailConfig:
    def __init__(self, configpath, debug=False):
        self.configpath = configpath
        self.config = self._get_config()
        self.debug=debug

    def _get_config(self):
        config = configparser.ConfigParser()
        config.read(self.configpath)
        return config

    def get_credential(self, section='DEFAULT'):
        config = self.config
        username = config[section]['username']
        password = config[section]['password']
        return username, password

    def get_access_token(self, section, refresh=False):
        config = self.config
        if refresh:
            return self.refresh_access_token(section)
        self.access_token = config[section]['access_token']
        return self.access_token

    def refresh_access_token(self, section):
        config = self.config
        self.user = config[section]['user']
        client_id = config[section]['client_id']
        client_secret = config[section]['client_secret']
        refresh_token = config[section]['refresh_token']
        # gmail oauth2.py is written for python 2
        ps = subprocess.run([
            os.path.join(os.path.dirname(__file__), './gmail/oauth2.py'),
            '--user={}'.format(self.user),
            '--client_id={}'.format(client_id),
            '--client_secret={}'.format(client_secret),
            '--refresh_token={}'.format(refresh_token)],
            stdout=subprocess.PIPE)
        access_token = ps.stdout.decode('utf-8').split('\n')[0].split(':')[1]
        if self.debug:
            print('접근 토큰: {}'.format(access_token))

        # update config file
        config[section]['access_token'] = access_token
        self.update_config(verbose=self.debug)

        self.access_token = access_token
        return access_token

    def update_config(self, verbose=False):
        config = self.config
        with open(self.configpath, 'w') as cf:
            config.write(cf)
        if verbose:
            print('Config file {} updated.'.format(self.configpath))


class EmailClient:
    def __init__(self,
        host,
        port=None,
        use_uid=True,
        ssl=False,
        stream=False,
        ssl_context=None,
        timeout=None,
        method=None,
        debug=False):
        self.debug = debug
        self._imapclient = IMAPClient(host, ssl=ssl)
        if method:
            if 'oauth2' in method:
                oauth2_config = method['oauth2']
                self.mailconfig = EmailConfig(oauth2_config['configfile'],
                    debug=self.debug)
                self.mailconfig.get_access_token('GMAIL', refresh=True)
                login_result = self.oauth2_login(self.mailconfig.user,
                    self.mailconfig.access_token)
                print(login_result)

    def oauth2_login(self, user, access_token):
        result = self._imapclient.oauth2_login(user, access_token)
        if 'Success' in result[0].decode('utf-8'):
            self.select_folder()
        return result

    def login(self, default_mailbox='INBOX', configfile=None):
        if configfile is None:
            username = input('이메일 계정: ')
            password = getpass.getpass(prompt='비밀번호: ')

        config = EmailConfig(configfile)
        username, password = config.get_credential()

        self._imapclient.login(username, password)
        return self.select_folder(folder = default_mailbox)

    def logout(self):
        return self._imapclient.logout()

    def select_folder(self, folder='INBOX', readonly=True):
        return self._imapclient.select_folder(folder, readonly=readonly)

    def search(self, criteria, charset='utf-8'):
        message_ids = self._imapclient.search(criteria, charset=charset)
        return message_ids

    def get_messages(self, message_ids):
        raw_messages = self._imapclient.fetch(message_ids, ['BODY[]'])
        messages=[]
        for mid, content in raw_messages.items():
            body = email.message_from_bytes(content[b'BODY[]'])
            messages.append((mid, body))
        return messages

    def get_subjects(self, message_ids):
        messages= self.get_messages(message_ids)
        subject_list = []
        for mid, msg in messages:
            message_header = dict()
            message_header['ID'] = mid
            message_header['FROM'] = self._decode_header(msg.get('FROM'))
            message_header['Subject'] = self._decode_header(msg.get('Subject'))[0]
            subject_list.append(message_header)
        return subject_list

    def _decode_header(self, header):
        content_list = []
        for field in email.header.decode_header(header):
            #if field is None: continue
            content, encoding = field
            if isinstance(content, bytes):
                content = content.decode(encoding if encoding else 'utf-8')
            content_list.append(content)
        return content_list

    def get_text(self, message_or_message_id):
        if type(message_or_message_id) == int:
            mid, message = self.get_messages(message_or_message_id)[0]

        for part in message.walk():
            content_type = part.get_content_type()
            if content_type.startswith('text'):
                text = part.get_payload(decode=True).decode('utf-8')
                yield content_type, text

    def show_attachments(self, message_or_message_id):
        if type(message_or_message_id) == int:
            mid, message = self.get_messages(message_or_message_id)[0]

        attachment_list = []
        if not message.is_multipart():
            return attachment_list

        for part in message.walk():
            content_type = part.get_content_type()
            if content_type.startswith('text'): continue
            filename = part.get_filename()
            if filename:
                attachment_list.append(filename)

        return attachment_list

    def download_attachments(self, message_or_message_id, target_dir=None):
        if type(message_or_message_id) == int:
            mid, message = self.get_messages(message_or_message_id)[0]

        file_list = []
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type.startswith('text'): continue
            filename = part.get_filename()
            if not filename: continue

            if target_dir:
                if not os.path.exists(target_dir):
                    raise FileNotFoundError('{} 경로가 존재하지 않습니다.'.format(target_dir))
                filename = os.path.join(target_dir, filename)

            with open(filename, 'wb') as f:
                f.write(part.get_payload(decode=True))
            file_list.append(os.path.abspath(filename))

        return file_list
