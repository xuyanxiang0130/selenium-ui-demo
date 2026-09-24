import logging
import os
from datetime import datetime

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
# logs文件夹已经建好，这里做兼容判断防止报错
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 日志文件名：时间戳命名
log_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".log"
LOG_FILE = os.path.join(LOG_DIR, log_filename)


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("selenium_ui_auto")
        self.logger.setLevel(logging.INFO)
        # 避免重复新增处理器（多次导入会重复打印日志的坑）
        if not self.logger.handlers:
            # 文件输出
            file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
            # 控制台输出
            console_handler = logging.StreamHandler()
            # 日志格式
            log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(log_format)
            console_handler.setFormatter(log_format)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)


# 全局单例，项目所有地方直接导入 log
log = Logger().logger
