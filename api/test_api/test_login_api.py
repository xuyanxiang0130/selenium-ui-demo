# 单独登录接口正向用例，直接调用 LoginApi，校验账号密码回传结果
import pytest
from api.api_pages.login_api import LoginApi
import allure

@pytest.mark.api
@pytest.mark.smoke
@allure.feature("接口测试模块")
@allure.story("用户登录模块")
@allure.title("账号密码登录，正向登录场景")
def test_login_api():
    login_api = LoginApi()
    resp = login_api.login("standard_user", "secret_sauce")
    # 断言响应码200
    assert resp.status_code == 200
    # httpbin会回传你提交的json，校验返回内容
    resp_json = resp.json()
    assert resp_json["json"]["username"] == "standard_user"
    assert resp_json["json"]["password"] == "secret_sauce"
