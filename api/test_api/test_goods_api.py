import pytest
from api.api_pages.goods_api import GoodsApi
from common.read_data import read_yaml

goods_data = read_yaml("api/api_data/goods_api_data.yaml")["goods_case"]

class TestGoodsApi:
    @pytest.mark.api
    @pytest.mark.parametrize("case", goods_data)
    def test_get_goods_list(self, case):
        """获取商品列表接口测试"""
        goods_api = GoodsApi()
        resp = goods_api.get_goods_list(page=case["page"], size=case["size"])
        # 断言状态码
        assert resp.status_code == case["expect_code"]
        # 额外业务断言：校验参数传递正确
        assert resp.json()["args"]["page"] == str(case["page"])
