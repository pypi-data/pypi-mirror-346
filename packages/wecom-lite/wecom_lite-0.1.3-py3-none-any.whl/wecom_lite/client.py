'''
通过企业微信API发送文本、文件、图片等消息。
'''
import sys
import time
import datetime
import os
import requests
from requests.adapters import Retry, HTTPAdapter
from .config import Config
from .logger import default_logger


class WeChat:
    '''
    企业微信API
    '''

    def __init__(self, token_file_path=None, logger=None):
        self.config = Config()
        self.config.validate()
        self.session = requests.Session()
        self.session.mount(
            'https://',
            HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.1)))
        # 设置令牌文件路径
        self.token_file_path = token_file_path or os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'tmp', 'access_token.conf')
        # 确保token文件目录存在
        os.makedirs(os.path.dirname(self.token_file_path), exist_ok=True)
        # 设置日志记录器
        self.logger = logger or default_logger

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {
            'corpid': self.config.CORP_ID,
            'corpsecret': self.config.CORP_SECRET
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("access_token")

    def get_access_token(self):
        '''
        获取token
        '''
        try:
            with open(self.token_file_path, 'r',
                      encoding='utf-8') as token_file:
                file_content = token_file.read().strip()
                if file_content:
                    epoch_timestamp, access_token = file_content.split()
                else:
                    raise ValueError("File is empty.")
        except (FileNotFoundError, ValueError):
            with open(self.token_file_path, 'w',
                      encoding='utf-8') as token_file:
                access_token = self._get_access_token()
                cur_time = time.time()
                token_file.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(epoch_timestamp) < 7260:
                return access_token
            else:
                with open(self.token_file_path, 'w',
                          encoding='utf-8') as token_file:
                    access_token = self._get_access_token()
                    token_file.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_text(self, msg):
        '''
        发送文本信息
        '''
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token(
        )
        send_values = {
            "touser": self.config.TOUSER,
            "msgtype": "text",
            "agentid": self.config.AGENT_ID,
            "text": {
                "content": msg
            },
            "safe": "0"
        }
        r = requests.post(send_url, json=send_values, timeout=10)
        # 记录发送结果
        self.logger.log_message_result("text",
                                       msg,
                                       r.content,
                                       touser=self.config.TOUSER,
                                       agent_id=self.config.AGENT_ID)
        return r.content

    def get_media_id(self):
        '''
        获取上传文件id
        '''
        post_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?type=file&access_token=' + self.get_access_token(
        )
        try:
            with open(self.FILEPATH, 'rb') as f:
                param = {'file': f}
                r = requests.post(post_url, files=param, timeout=10)
        except IOError:
            print('要推送的文件不存在！')
            sys.exit()
        return r.json()['media_id']

    def send_files(self, file_path):
        '''
        发送文件
        '''
        WeChat.FILEPATH = file_path
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token(
        )
        send_values = {
            "touser": self.config.TOUSER,
            "msgtype": "file",
            "agentid": self.config.AGENT_ID,
            "file": {
                "media_id": self.get_media_id()
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        r = requests.post(send_url, json=send_values, timeout=10)
        # 记录发送结果
        self.logger.log_message_result("file",
                                       file_path,
                                       r.content,
                                       touser=self.config.TOUSER,
                                       agent_id=self.config.AGENT_ID)
        return r.content

    def send_images(self, file_path):
        '''
        发送图片
        '''
        WeChat.FILEPATH = file_path
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token(
        )
        send_values = {
            "touser": self.config.TOUSER,
            "msgtype": "image",
            "agentid": self.config.AGENT_ID,
            "image": {
                "media_id": self.get_media_id()
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        r = requests.post(send_url, json=send_values, timeout=10)
        # 记录发送结果
        self.logger.log_message_result("image",
                                       file_path,
                                       r.content,
                                       touser=self.config.TOUSER,
                                       agent_id=self.config.AGENT_ID)
        return r.content

    def send_textcard(self, url, title, description):
        '''
        发送文本卡片
        '''
        WeChat.URL = url
        today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token(
        )
        send_values = {
            "touser": self.config.TOUSER,
            "msgtype": "textcard",
            "agentid": self.config.AGENT_ID,
            "textcard": {
                "title":
                title,
                "description":
                description + "\n<div class=\"highlight\">" + today + "</div>",
                "url":
                WeChat.URL,
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        r = requests.post(send_url, json=send_values, timeout=10)
        # 记录发送结果
        self.logger.log_message_result("textcard",
                                       f"{title}: {description}",
                                       r.content,
                                       url=url,
                                       touser=self.config.TOUSER,
                                       agent_id=self.config.AGENT_ID)
        return r.content

    def send_markdown(self, des):
        '''
        发送markdown消息
        '''
        today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token(
        )
        send_values = {
            "touser": self.config.TOUSER,
            "msgtype": "markdown",
            "agentid": self.config.AGENT_ID,
            "markdown": {
                "content": f'{des}\n{today}',
            },
            "safe": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        r = requests.post(send_url, json=send_values, timeout=10)
        # 记录发送结果
        self.logger.log_message_result("markdown",
                                       des,
                                       r.content,
                                       touser=self.config.TOUSER,
                                       agent_id=self.config.AGENT_ID)
        return r.content
