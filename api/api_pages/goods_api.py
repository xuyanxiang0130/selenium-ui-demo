import requests
from common.logger import log

class GoodsApi:
    base_url = "http://httpbin.org"

    def get_goods_list(self, page=1, size=10):
        """模拟获取商品列表GET接口"""
        url = f"{self.base_url}/get"
        # GET请求用params传参
        params = {
            "page": page,
            "size": size
        }
        log.info(f"【接口请求】GET {url}, 查询参数：page={page},size={size}")
        resp = requests.get(url=url, params=params)
        log.info(f"【接口响应】状态码：{resp.status_code}, 返回参数：{resp.json()['args']}")
        return resp
