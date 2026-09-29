import os
from common.read_data import read_yaml

# 获取项目根目录
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 配置yaml完整路径
CONFIG_FILE_PATH = os.path.join(ROOT_PATH, "data", "config.yaml")


def get_env_config(key: str = None, env: str = None):
    """
    获取环境配置
    :param key: 配置的key，不传返回整个环境配置
    :param env: 指定环境 dev/test；不传则读取yaml里默认环境
    :return: 配置值
    """
    all_config = read_yaml(CONFIG_FILE_PATH)
    # ==========新增逻辑：区分 数据库配置 和 env普通配置 ==========
    # 如果key是db_config，直接取顶层的db_config，不需要进env_config
    if key == "db_config":
        if env is None:
            env = all_config.get("env")
        return all_config["db_config"][env]

    # 下面是原来读取 base_url / timeout 的逻辑，不动
    # 如果传了env参数，优先使用传入的环境；否则读取yaml默认env
    if env is None:
        current_env = all_config.get("env")
    else:
        current_env = env
    env_info = all_config["env_config"][current_env]

    if key:
        return env_info.get(key)
    return env_info


# 本地调试入口
if __name__ == "__main__":
    # 1. 读取yaml默认环境（test环境，saucedemo，给UI用）
    base_url_test = get_env_config("base_url")
    timeout_test = get_env_config("timeout")
    print(f"yaml默认环境【test】base_url：{base_url_test}")

    # 2. 手动指定dev环境（httpbin，给接口用）
    base_url_dev = get_env_config("base_url", env="dev")
    timeout_dev = get_env_config("timeout", env="dev")
    print(f"手动指定环境【dev】base_url：{base_url_dev}")

    # ✅ 新增调试：读取数据库配置，验证密码等信息
    db_dev_conf = get_env_config("db_config", env="dev")
    print(f"\ndev环境数据库配置：{db_dev_conf}")
