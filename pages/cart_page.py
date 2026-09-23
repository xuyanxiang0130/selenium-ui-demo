from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    # ========== 页面元素定位器 ==========
    cart_item_loc = (By.CLASS_NAME, "cart_item")
    item_name_loc = (By.CLASS_NAME, "inventory_item_name")
    remove_btn_loc = (By.CSS_SELECTOR, ".cart_item button")
    checkout_btn_loc = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ========== 页面操作方法 ==========
    def get_cart_item_count(self):
        """获取购物车里商品数量"""
        try:
            items = self.wait.until(EC.presence_of_all_elements_located(self.cart_item_loc))
            return len(items)
        except:
            return 0

    def get_first_item_name(self):
        """获取第一个商品的名称"""
        name_elem = self.wait.until(EC.presence_of_element_located(self.item_name_loc))
        return name_elem.text

    def remove_first_item(self):
        """移除第一个商品"""
        self.wait.until(EC.element_to_be_clickable(self.remove_btn_loc)).click()

    def click_checkout(self):
        """点击结算按钮"""
        elem = self.wait.until(EC.element_to_be_clickable(self.checkout_btn_loc))
        elem.click()
