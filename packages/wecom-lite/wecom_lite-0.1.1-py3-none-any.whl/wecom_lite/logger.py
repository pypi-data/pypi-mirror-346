"""
日志记录模块，用于记录消息发送等操作的结果
"""
import os
import logging
import json
from datetime import datetime


class Logger:
    """日志记录器，负责记录企业微信消息发送的结果"""

    def __init__(self, log_dir=None):
        """
        初始化日志记录器
        
        Args:
            log_dir: 日志文件存储目录，默认为项目根目录下的logs
        """
        # 设置日志目录
        self.log_dir = log_dir or os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'logs')
        # 确保日志目录存在
        os.makedirs(self.log_dir, exist_ok=True)

        # 配置日志记录器
        self.logger = logging.getLogger('wecom_lite')
        self.logger.setLevel(logging.INFO)

        # 避免重复处理器
        if not self.logger.handlers:
            # 文件处理器 - 记录所有日志
            log_file = os.path.join(self.log_dir, 'wecom.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)

            # 格式化日志消息
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # 添加处理器到记录器
            self.logger.addHandler(file_handler)

    def log_message_result(self, msg_type, content, result, **kwargs):
        """
        记录消息发送结果
        
        Args:
            msg_type: 消息类型，如text, image, file等
            content: 消息内容或描述
            result: API返回的结果
            **kwargs: 其他需要记录的信息
        """
        try:
            # 解析结果
            if isinstance(result, bytes):
                result_dict = json.loads(result.decode('utf-8'))
            elif isinstance(result, str):
                result_dict = json.loads(result)
            else:
                result_dict = {"raw_result": str(result)}

            # 构建日志内容
            log_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "msg_type": msg_type,
                "content": content,
                "result": result_dict,
            }

            # 添加额外信息
            if kwargs:
                log_data.update(kwargs)

            # 记录日志
            status = "成功" if result_dict.get("errcode") == 0 else "失败"
            self.logger.info(
                f"发送{msg_type}消息{status}: {json.dumps(log_data, ensure_ascii=False)}"
            )

            # 单独写入详细日志文件（便于分析）
            detailed_log_file = os.path.join(
                self.log_dir,
                f'wecom_details_{datetime.now().strftime("%Y%m%d")}.log')
            with open(detailed_log_file, 'a', encoding='utf-8') as f:
                f.write(f"{json.dumps(log_data, ensure_ascii=False)}\n")

            return True
        except Exception as e:
            self.logger.error(f"记录日志失败: {str(e)}")
            return False


# 创建默认日志记录器实例
default_logger = Logger()
