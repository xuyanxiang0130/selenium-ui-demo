import yaml
from common.logger import log

def get_yaml_data(file_path):
    """读取yaml文件，返回字典"""
    log.info(f"读取测试数据文件: {file_path}")
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f)
