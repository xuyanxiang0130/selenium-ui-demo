# 接口依赖场景，pytest fixture 前置登录，
# 自动获取并携带 token，鉴权接口测试
import pytest
from common.assert_util import AssertUtil
import allure
class TestUserInfoApi:
    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.rerun(reruns=2, reruns_delay=1)
    @allure.feature("接口测试模块")
    @allure.story("用户鉴权模块")
    @allure.title("携带有效token，成功获取用户信息")
    def test_get_user_with_token(self, logged_in_user_api):
        """
        参数带 logged_in_user_api，自动执行前置登录逻辑，直接拿到带token的接口对象
        不用自己写登录、传token，用例只需要写业务调用和断言
        """
        # 直接调用方法，接口已经自动带了Authorization头
        resp = logged_in_user_api.get_user_info()
        json_data = resp.json()
        headers_data = json_data["headers"]
        # 使用封装好的断言工具
        AssertUtil.assert_status_code(resp, 200)
        AssertUtil.assert_json_key_exist(headers_data, "Authorization")
        AssertUtil.assert_json_value(headers_data, "Authorization", "Bearer abcdefg123456789token")