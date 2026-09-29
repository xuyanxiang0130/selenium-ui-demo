from api.api_pages.api_base import BaseApi

class GoodsApi(BaseApi):
    def get_goods_list(self, page, size):
        """获取商品列表接口"""
        url_path = "/get"
        params = {
            "page": page,
            "size": size
        }
        resp = self.send_request(method="GET", url_path=url_path,params=params)
        return resp

    # 追加到你现有的 GoodsApi 类里面，新增两个方法
    def add_goods(self, goods_name, price):
        """新增商品接口，用来造测试数据"""
        url_path = "/post"
        data = {
            "goods_name": goods_name,
            "price": price
        }
        resp = self.send_request("POST", url_path=url_path, data=data)
        return resp

    def delete_goods(self, goods_id):
        """删除商品接口，清理测试数据"""
        url_path = "/delete"
        data = {
            "goods_id": goods_id
        }
        resp = self.send_request("DELETE", url_path=url_path, data=data)
        return resp
