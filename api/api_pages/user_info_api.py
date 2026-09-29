import requests
from common.logger import log
from api.api_pages.api_base import BaseApi
class UserInfoApi(BaseApi):
    def get_user_info(self):
        """需要token鉴权：获取用户信息接口"""
        url_path = "/headers"
        resp = self.send_request(method="GET", url_path=url_path)
        return resp
