import pytest
from api.api_pages.login_api import LoginApi
from common.read_data import read_yaml

# 读取yaml接口测试数据
login_data = read_yaml("api/api_data/login_api_data.yaml")["login_case"]

class TestLoginApi:
    @pytest.mark.api
    @pytest.mark.parametrize("case", login_data)
    def test_post_login(self, case):
        """模拟登录接口测试"""
        login_api = LoginApi()
        resp = login_api.post_login(username=case["username"], password=case["password"])
        # 断言：预期状态码
        assert resp.status_code == case["expect_code"]
