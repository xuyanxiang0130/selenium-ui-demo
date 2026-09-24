import requests
from common.logger import log

class LoginApi:
    base_url = "http://httpbin.org"

    def post_login(self, username, password):
        """模拟登录POST接口"""
        url = f"{self.base_url}/post"
        log.info(f"【接口请求】POST {url}, 请求参数：username={username},pwd={password}")
        payload = {
            "username": username,
            "password": password
        }
        resp = requests.post(url=url, json=payload)
        log.info(f"【接口响应】状态码：{resp.status_code}, 返回内容：{resp.json()}")
        return resp
