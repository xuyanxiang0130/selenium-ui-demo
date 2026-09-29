from common.logger import logger
import allure
class AssertUtil:
    @staticmethod
    def assert_status_code(resp, expect_code):
        """断言状态响应码"""
        with allure.step(f"断言状态码，预期：{expect_code}"):
            logger.info(f"断言状态码：预期{expect_code}，实际：{resp.status_code}")
            assert resp.status_code == expect_code, f"状态码不一致！预期：{expect_code},实际：{resp.status_code},响应内容：{resp.text}"

    @staticmethod
    def assert_json_key_exist(json_data, key_name):
        """断言json返回包含某个key"""
        with allure.step(f"断言JSON存在key：{key_name}"):
            logger.info(f"断言json存在key：{key_name}")
            assert key_name in json_data, f"返回结果不存在key【{key_name}】，返回数据：{json_data}"

    @staticmethod
    def assert_json_value(json_data, key_name, expect_value):
        """断言中json中key的值等于期望值"""
        with allure.step(f"断言key【{key_name}】的值 = {expect_value}"):
            logger.info(f"断言key:{key_name},预期值：{expect_value}，实际值：{json_data.get(key_name)}")
            real_val = json_data.get(key_name)
            assert real_val == expect_value, f"值不匹配！key:{key_name},预期:{expect_value},实际：{real_val}"

    @staticmethod
    def assert_json_contains(json_data, expect_str):
        """断言响应包含指定字符串"""
        with allure.step(f"断言JSON包含字符串：{expect_str}"):
            logger.info(f"断言响应字段包含字符串：{expect_str}")
            assert expect_str in str(json_data), f"返回结果不包含【{expect_str}】,返回：{json_data}"
