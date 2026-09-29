# 统一封装 HTTP 请求，自动拼接地址、带 token、
# 打日志、自动把请求 / 响应塞进 Allure 报告，
# 上层写业务接口和测试用例时不用重复写 requests、日志、allure 附件代码
import requests
from common.get_env_config import get_env_config
from common.logger import logger
import allure

class BaseApi:
    def __init__(self):
        # 初始化：读取全局base_url和超时
        # 接口框架固定使用dev环境 httpbin.org
        env_config_dict = get_env_config(env=GLOBAL_ENV)
        self.base_url = env_config_dict["base_url"]
        self.timeout = env_config_dict["timeout"]
        # 实例变量，每个对象自己的token
        self.token = None
        # 统一请求头，后续接口可以覆盖
        self.headers = {
            "Content-Type": "application/json"
        }
# 所有请求调用这个方法
    def send_request(self, method, url_path, data=None, params=None, headers=None):
        """
        统一发送http请求
        :param method: 请求方法 GET / POST
        :param url_path: 接口路径（不是完整url，例如：/api/login）
        :param data: 请求体，字典
        :param params: url查询参数
        :param headers: 自定义请求头
        :return: response对象
        """
        # 拼接完整url
        full_url = self.base_url + url_path
        # 如果传入自定义headers就覆盖默认
        req_headers = headers.copy() if headers else self.headers.copy()

        # 使用当前实例自己的token
        logger.info(f"【DEBUG】当前实例self.token的值：{self.token}")
        if self.token:
            req_headers["Authorization"] = f"Bearer {self.token}"

        logger.info(f" 发起{method}请求 ")
        logger.info(f"请求地址：{full_url}")
        logger.info(f"请求头：{req_headers}")
        logger.info(f"请求body：{data}")
        logger.info(f"请求params：{params}")
        # 请求信息嵌入allure报告
        allure.attach(
            f"请求地址：{full_url}\n请求头：{req_headers}\n请求体：{data}\n请求参数：{params}",
            name="接口请求详情",
            attachment_type=allure.attachment_type.TEXT
        )

        try:
            resp = requests.request(
                method=method,
                url=full_url,
                json=data,
                params=params,
                headers=req_headers,
                timeout=self.timeout
            )
            logger.info(f"响应状态码：{resp.status_code}")
            logger.info(f"响应内容：{resp.text}")
            # 响应信息嵌入allure报告
            allure.attach(
                f"响应状态码：{resp.status_code}\n响应内容：{resp.text}",
                name="接口响应详情",
                attachment_type=allure.attachment_type.TEXT
            )
            return resp
        except requests.exceptions.RequestException as e:
            logger.error(f"接口请求异常：{str(e)}")
            raise

    def save_token(self, token):
        self.token = token
        logger.info(f"全局token已保存：{token}")

