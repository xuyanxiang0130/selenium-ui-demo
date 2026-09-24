import pytest
import yaml
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from common.logger import log

def get_cart_data():
    with open("./data/cart_data.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    case_list = []
    for case in data["cart_cases"]:
        case_tag = case.get("tag", "smoke")
        if case_tag == "smoke":
            marks = pytest.mark.smoke
        elif case_tag == "negative":
            marks = pytest.mark.negative
        else:
            marks = pytest.mark.regression
        case_list.append(
            pytest.param(
                case["case_name"],
                case["action"],
                case.get("add_item_name", None),
                case.get("expect_item_count", None),
                case.get("expect_name_keyword", None),
                case.get("expect_url_keyword", None),
                marks=marks
            )
        )
    return case_list


@pytest.mark.parametrize(
    "case_name, action, add_item_name, expect_item_count, expect_name_keyword, expect_url_keyword",
    get_cart_data()
)

def test_cart(case_name, action, add_item_name, expect_item_count, expect_name_keyword, expect_url_keyword, driver):
    log.info(f"\n=====执行用例：{case_name}=====")
    # 前置：登录系统，进入商品页
    login_page = LoginPage(driver)
    login_page.open_url()
    login_page.login("standard_user", "secret_sauce")

    inv_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    # 添加商品，进入购物车
    log.info(f"添加商品【{add_item_name}】并进入购物车页面")
    inv_page.add_item_by_name(add_item_name)
    inv_page.go_to_cart()

    # 不同业务分支判断
    if action == "add_item_check_count":
        count = cart_page.get_cart_item_count()
        assert count == expect_item_count, f"购物车数量不对，实际:{count},预期:{expect_item_count}"
        log.info(f"【{case_name}】用例执行通过")

    elif action == "check_item_name":
        item_name = cart_page.get_first_item_name()
        assert expect_name_keyword in item_name, f"商品名称校验失败，页面名称:{item_name}"
        log.info(f"【{case_name}】用例执行通过")

    elif action == "remove_item_check_empty":
        cart_page.remove_first_item()
        count = cart_page.get_cart_item_count()
        assert count == expect_item_count, f"删除后购物车数量不对，实际:{count},预期:{expect_item_count}"
        log.info(f"【{case_name}】用例执行通过")

    elif action == "go_to_checkout":
        cart_page.click_checkout()
        assert expect_url_keyword in driver.current_url, f"页面跳转失败，当前url:{driver.current_url}"
        log.info(f"【{case_name}】用例执行通过")
