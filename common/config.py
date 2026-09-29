import os
from common.read_data import read_yaml

# 获取项目根目录
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置yaml完整路径
CONFIG_FILE_PATH = os.path.join(ROOT_PATH, "data", "config.yaml")


def get_env_config(key: str = None):
    """
    获取环境配置
    :param key: 配置的key，不传返回整个环境配置
    :return: 配置值
    """
    all_config = read_yaml(CONFIG_FILE_PATH)
    current_env = all_config.get("env")
    env_info = all_config["env_config"][current_env]

    if key:
        return env_info.get(key)
    return env_info


# 本地调试入口
if __name__ == "__main__":
    base_url = get_env_config("base_url")
    timeout = get_env_config("timeout")
    print(f"当前环境base_url：{base_url}")
    print(f"请求超时时间：{timeout}")
