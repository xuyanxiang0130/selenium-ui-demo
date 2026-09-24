import pytest
from api.api_pages.login_api import LoginApi
from api.api_pages.user_info_api import UserInfoApi

class TestUserInfoApi:
    @pytest.mark.api
    def test_get_user_with_token(self):
        """流程：先登录拿到token，再携带token查询用户信息（接口串联）"""
        # 1.执行登录
        login_api = LoginApi()
        login_resp = login_api.post_login(username="test", password="123456")
        assert login_resp.status_code == 200

        # 模拟后端返回token，真实项目这里从login_resp.json()拿token
        token = "abcdefg123456789token"

        # 2.携带token调用获取用户信息接口
        user_api = UserInfoApi()
        resp = user_api.get_user_info(token=token)

        # 断言：请求头里面带上了Bearer token
        assert resp.status_code == 200
        assert "Bearer abcdefg123456789token" in resp.json()["headers"]["Authorization"]
