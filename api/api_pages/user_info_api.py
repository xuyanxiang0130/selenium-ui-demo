import requests
from common.logger import log

class UserInfoApi:
    base_url = "http://httpbin.org"

    def get_user_info(self, token):
        """需要token鉴权：获取用户信息接口"""
        url = f"{self.base_url}/headers"
        # 请求头，把token放到headers里面
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        log.info(f"【接口请求】GET {url}, headers={headers}")
        resp = requests.get(url=url, headers=headers)
        log.info(f"【接口响应】状态码：{resp.status_code}, 返回内容：{resp.json()}")
        return resp
