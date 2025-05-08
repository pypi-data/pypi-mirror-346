from dotenv import load_dotenv
import os


class Config:

    def __init__(self):
        load_dotenv()
        self.CORP_ID = os.getenv('WECOM_CORP_ID')
        self.CORP_SECRET = os.getenv('WECOM_SECRET')
        self.AGENT_ID = int(os.getenv('WECOM_AGENT_ID'))
        self.TOUSER = os.getenv('WECOM_TOUSER')

    def validate(self):
        """验证必要的配置是否存在"""
        if not all([self.CORP_ID, self.CORP_SECRET, self.AGENT_ID]):
            raise ValueError("请检查配置文件 .env 中是否包含所有必要的配置项")
