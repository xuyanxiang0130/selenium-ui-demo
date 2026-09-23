import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from common.read_data import get_yaml_data

data = get_yaml_data("data/checkout_data.yaml")

def test_checkout_full_flow(logged_in_driver):
    """完整下单流程，从加购到下单成功"""
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

    assert data["checkout_success_msg_keyword"] in checkout_page.get_complete_message()

def test_checkout_empty_info(logged_in_driver):
    """结算页不填信息提交，校验报错"""
    inv_page = InventoryPage(logged_in_driver)
    inv_page.add_backpack_to_cart()
    inv_page.go_to_cart()
    cart_page = CartPage(logged_in_driver)
    cart_page.click_checkout()

    checkout_page = CheckoutPage(logged_in_driver)
    checkout_page.click_continue()
    assert data["checkout_error_keyword"] in logged_in_driver.page_source
