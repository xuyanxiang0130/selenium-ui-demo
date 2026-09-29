from api.api_pages.api_base import BaseApi

class HttpApi(BaseApi):
    def api_get(self, params=None, headers=None):
        """httpbin的GET接口 /get"""
        return self.send_request(
            method="GET",
            url_path="/get",
            params=params,
            headers=headers
        )

    def api_post_json(self, data=None, headers=None):
        """httpbin的POST json接口 /post"""
        return self.send_request(
            method="POST",
            url_path="/post",
            data=data,
            headers=headers
        )

    def api_404(self):
        """请求不存在的接口路径，测试404状态码"""
        return self.send_request(
            method="GET",
            url_path="/not_exist_path_404"
        )
