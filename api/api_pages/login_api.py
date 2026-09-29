from api.api_pages.api_base import BaseApi

class LoginApi(BaseApi):
    def login(self, username, password):
        # httpbin的post接口，用来接收post请求，原样返回提交的数据
        url_path = "/post"
        json_data = {
            "username": username,
            "password": password
        }
        resp = self.send_request(method="POST", url_path=url_path, data=json_data)
        # 模拟提取token，存入当时login_api实例，真实业务：token = resp.json()["token"]
        token = "abcdefg123456789token"
        self.save_token(token)
        return resp
