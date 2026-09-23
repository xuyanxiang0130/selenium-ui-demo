import pytest
import yaml
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 和登录模块一模一样：读取yaml，转元组列表
def get_inventory_data():
    with open("./data/inventory_data.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    case_list = []
    for case in data["inventory_cases"]:
        # .get() 取不到字段返回None，解决KeyError
        case_list.append(
            (
                case["case_name"],
                case["action"],
                case.get("expect_title", None),
                case.get("expect_goods_num", None),
                case.get("expect_first_name", None),
                case.get("expect_first_price", None)
            )
        )
    return case_list


@pytest.mark.parametrize("case_name,action,expect_title,expect_goods_num,expect_first_name,expect_first_price", get_inventory_data())
def test_inventory(case_name,action,expect_title,expect_goods_num,expect_first_name,expect_first_price, driver):
    print(f"\n=====执行用例：{case_name}=====")
    # 前置操作：登录
    login_page = LoginPage(driver)
    login_page.open_url()
    login_page.login("standard_user", "secret_sauce")

    inv_page = InventoryPage(driver)

    if action == "check_page_info":
        # 等待商品页面标题
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "title"))
        )
        title_text = inv_page.get_title()
        goods_items = inv_page.get_all_items()
        assert title_text == expect_title
        assert len(goods_items) == expect_goods_num

    elif action == "sort_name_asc":
        inv_page.select_sort("Name (A to Z)")
        first_item = inv_page.get_first_item_name()
        assert first_item == expect_first_name

    elif action == "sort_price_asc":
        inv_page.select_sort("Price (low to high)")
        first_item_price = inv_page.get_first_item_price()
        assert first_item_price == expect_first_price
