#纯基础 GET/POST/404 异常场景， yaml 读取多组数据，pytest 参数化，用来演示数据驱动
import pytest
from api.api_pages.http_api import HttpApi
from common.read_data import read_yaml
import allure

# 读取接口yaml测试数据
api_test_data = read_yaml("api/api_data/api_test_data.yaml")

# 组装成pytest参数化需要的元组列表
get_cases = [
    (item["case_name"], item["params"], item["expect_code"])
    for item in api_test_data["test_get"]
]

post_cases = [
    (item["case_name"], item["data"], item["expect_code"])
    for item in api_test_data["test_post"]
]


@pytest.mark.parametrize("case_name, params, expect_code", get_cases)
@allure.feature("接口测试模块")
@allure.story("http基础接口")
@allure.title("{case_name}")
def test_http_get_case(case_name, params, expect_code, request):
    """httpbin GET接口多场景数据驱动测试"""
    http_api = HttpApi()
    resp = http_api.api_get(params=params)
    # 挂载resp，conftest钩子失败时抓取报文
    request.node.resp = resp

    # 基础断言：状态码
    assert resp.status_code == expect_code
    resp_json = resp.json()
    # 有参数的时候，校验回显的参数是否一致
    if params is not None:
        expected_args = {k: str(v) for k, v in params.items()}
        assert resp_json["args"] == expected_args


@pytest.mark.parametrize("case_name, data, expect_code", post_cases)
@allure.feature("接口测试模块")
@allure.story("Http基础接口")
@allure.title("{case_name}")
def test_http_post_case(case_name, data, expect_code, request):
    """httpbin POST JSON接口多场景数据驱动测试"""
    http_api = HttpApi()
    resp = http_api.api_post_json(data=data)
    # 挂载resp
    request.node.resp = resp

    assert resp.status_code == expect_code
    resp_json = resp.json()
    assert resp_json["json"] == data


@pytest.mark.api
@pytest.mark.smoke
@allure.feature("接口测试模块")
@allure.story("Http基础接口")
@allure.title("异常场景：访问不存在地址，校验404")
def test_http_404_case(request):
    """异常场景：访问不存在的接口，断言返回404"""
    http_api = HttpApi()
    resp = http_api.api_404()
    request.node.resp = resp
    assert resp.status_code == 404


#
