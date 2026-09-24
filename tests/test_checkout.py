import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from common.read_data import get_yaml_data
from common.logger import log

data = get_yaml_data("data/checkout_data.yaml")


@pytest.mark.smoke
def test_checkout_full_flow(logged_in_driver):
    """完整下单流程，从加购到下单成功【smoke主干用例】"""
    log.info("\n=====执行用例：完整下单全流程=====")
    inv_page = InventoryPage(logged_in_driver)
    inv_page.add_backpack_to_cart()
    inv_page.go_to_cart()
    cart_page = CartPage(logged_in_driver)
    cart_page.click_checkout()

    checkout_page = CheckoutPage(logged_in_driver)
    # 从yaml读取收货信息
    info = data["checkout_valid_info"]
    checkout_page.fill_info(info["firstname"], info["lastname"], info["postal_code"])
    checkout_page.click_continue()
    checkout_page.click_finish()

    success_msg = checkout_page.get_complete_message()
    assert data["checkout_success_msg_keyword"] in success_msg
    log.info("【完整下单全流程】用例执行通过")


@pytest.mark.negative
def test_checkout_empty_info(logged_in_driver):
    """结算页不填信息提交，校验报错【negative异常用例】"""
    log.info("\n=====执行用例：结算不填信息提交，校验错误提示=====")
    inv_page = InventoryPage(logged_in_driver)
    inv_page.add_backpack_to_cart()
    inv_page.go_to_cart()
    cart_page = CartPage(logged_in_driver)
    cart_page.click_checkout()

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.click_continue()
    assert data["checkout_error_keyword"] in logged_in_driver.page_source
    log.info("【结算空信息校验】用例执行通过")
