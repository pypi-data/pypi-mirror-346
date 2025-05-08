"""轻量级企业微信消息发送库"""

from .client import WeChat
from .config import Config
from .logger import Logger, default_logger

__version__ = "0.1.1"
__all__ = ["WeChat", "Config", "Logger", "default_logger"]
