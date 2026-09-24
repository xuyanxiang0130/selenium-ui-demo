from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.logger import log

class InventoryPage:
    # 元素定位
    title_loc = (By.CLASS_NAME, "title")
    item_name_loc = (By.CLASS_NAME, "inventory_item_name")
    item_price_loc = (By.CLASS_NAME, "inventory_item_price")
    sort_select_loc = (By.CLASS_NAME, "product_sort_container")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.item_name_loc = (By.CLASS_NAME, "inventory_item_name")
        # 添加购物车按钮
        self.add_btn_template = "//div[text()='{}']/ancestor::div[@class='inventory_item']//button"
        log.info("实例化商品列表页面对象")

    def add_item_by_name(self, item_name):
        # 根据商品名称定位【加入购物车】按钮
        log.info(f"添加商品：{item_name} 到购物车")
        loc = (By.XPATH, self.add_btn_template.format(item_name))
        self.wait.until(EC.element_to_be_clickable(loc)).click()

    def go_to_cart(self):
        """点击右上角购物车图标，进入购物车页面"""
        log.info("点击右上角购物车图标，跳转购物车页面")
        cart_icon_loc = (By.CLASS_NAME, "shopping_cart_link")
        self.wait.until(EC.element_to_be_clickable(cart_icon_loc)).click()

    def get_title(self):
        log.info("获取商品页面标题")
        title_elem = self.wait.until(EC.presence_of_element_located(self.title_loc))
        title_text = title_elem.text
        log.info(f"页面标题为：{title_text}")
        return title_text

    def get_all_items(self):
        log.info("获取页面全部商品列表")
        item_list = self.wait.until(EC.presence_of_all_elements_located(self.item_name_loc))
        log.info(f"页面商品总数：{len(item_list)}")
        return item_list

    def select_sort(self, option_text):
        from selenium.webdriver.support.ui import Select
        log.info(f"商品列表选择排序方式：{option_text}")
        sort_elem = self.wait.until(EC.element_to_be_clickable(self.sort_select_loc))
        select = Select(sort_elem)
        select.select_by_visible_text(option_text)

    def get_first_item_name(self):
        log.info("获取列表第一个商品名称")
        items = self.wait.until(EC.presence_of_all_elements_located(self.item_name_loc))
        name = items[0].text
        log.info(f"首个商品名称：{name}")
        return name

    def get_first_item_price(self):
        log.info("获取列表第一个商品价格")
        price_items = self.wait.until(EC.presence_of_all_elements_located(self.item_price_loc))
        price = price_items[0].text
        log.info(f"首个商品价格：{price}")
        return price

    def add_backpack_to_cart(self):
        """添加Sauce Labs Backpack背包到购物车"""
        log.info("添加 Sauce Labs Backpack 背包商品到购物车")
        # 定位背包对应的加入购物车按钮
        backpack_add_btn = (
        By.XPATH, "//div[text()='Sauce Labs Backpack']/ancestor::div[@class='inventory_item']//button")
        self.wait.until(EC.element_to_be_clickable(backpack_add_btn)).click()
