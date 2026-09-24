import pytest
import yaml
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 导入日志
from common.logger import log


# 读取yaml数据，真正的数据驱动：代码和用例数据分离
def get_login_data():
    with open("./data/login_data.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    case_list = []
    for case in data["login_cases"]:
        # 读取这条用例的tag，默认是smoke
        case_tag = case.get("tag", "smoke")
        # 根据tag，给这条用例单独打mark
        if case_tag == "smoke":
            marks = pytest.mark.smoke
        elif case_tag == "negative":
            marks = pytest.mark.negative
        else:
            marks = pytest.mark.regression
        # 用pytest.param包装，单独给这条用例加标签
        case_list.append(
            pytest.param(
                case["case_name"], case["username"], case["password"], case["expect"],
                marks=marks
            )
        )
    return case_list



@pytest.mark.parametrize("case_name,username,password,expect_result", get_login_data())
def test_login(case_name, username, password, expect_result, driver):
    login_page = LoginPage(driver)
    login_page.open_url()
    log.info(f"\n=====执行用例：{case_name}=====")

    if expect_result == "empty_user":
        login_page.enter_password(password)
        login_page.click_login()
    elif expect_result == "empty_pwd":
        login_page.enter_username(username)
        login_page.click_login()
    else:
        login_page.login(username, password)

    # 断言逻辑不变
    if expect_result == "success":
        log.info("断言：预期登录成功，等待商品页面标题")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        assert "Products" in driver.page_source
        log.info(f"【{case_name}】用例执行通过")
    else:
        error_text = login_page.get_error_msg()
        assert error_text != ""
        log.info(f"【{case_name}】用例执行通过，成功捕获错误提示")
