# 参数化 + yaml 数据驱动，测试商品列表接口，
# 不同 page/size 参数，校验接口回传的分页参数。
import pytest
from api.api_pages.goods_api import GoodsApi
from common.read_data import read_yaml
import allure
from common.logger import logger

goods_data = read_yaml("api/api_data/goods_api_data.yaml")["goods_case"]

class TestGoodsApi:
    @pytest.mark.api
    @pytest.mark.smoke
    @allure.feature("接口测试模块")
    @allure.story("商品模块")
    @allure.title("多组分页参数获取商品列表(数据隔离+数据库断言)")
    @pytest.mark.parametrize("case", goods_data)
    def test_get_goods_list(self, case, temp_goods_fixture,db_client):
        """获取商品列表接口测试"""
        goods_api = GoodsApi()
        goods_id, goods_name, price = temp_goods_fixture
        _ = goods_id

        resp = goods_api.get_goods_list(page=case["page"], size=case["size"])
        # 断言状态码
        assert resp.status_code == case["expect_code"]
        # 额外业务断言：校验参数传递正确
        assert resp.json()["args"]["page"] == str(case["page"])

        # ✅ 新增数据库断言：去数据库查询商品，校验名称和价格
        sql = "SELECT * FROM goods WHERE goods_name=%s"
        db_result = db_client.query_one(sql, args=(goods_name,))
        logger.info(f"【DB查询结果】{db_result}")
        assert db_result["goods_name"] == goods_name
        assert float(db_result["price"]) == price
        logger.info("✅数据库校验通过，接口存储数据和数据库一致")
