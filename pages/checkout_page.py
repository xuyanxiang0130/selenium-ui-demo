from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    # 元素定位
    first_name_loc = (By.ID, "first-name")
    last_name_loc = (By.ID, "last-name")
    postal_code_loc = (By.ID, "postal-code")
    continue_btn_loc = (By.ID, "continue")
    finish_btn_loc = (By.ID, "finish")
    complete_msg_loc = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)

    def fill_info(self, firstname, lastname, postal_code):
        """填写结算收货信息"""
        self.wait.until(EC.element_to_be_clickable(self.first_name_loc)).send_keys(firstname)
        self.wait.until(EC.element_to_be_clickable(self.last_name_loc)).send_keys(lastname)
        self.wait.until(EC.element_to_be_clickable(self.postal_code_loc)).send_keys(postal_code)

    def click_continue(self):
        """点击continue按钮"""
        self.wait.until(EC.element_to_be_clickable(self.continue_btn_loc)).click()

    def click_finish(self):
        """点击finish完成下单"""
        self.wait.until(EC.element_to_be_clickable(self.finish_btn_loc)).click()

    def get_complete_message(self):
        """获取下单成功提示文本"""
        msg_elem = self.wait.until(EC.presence_of_element_located(self.complete_msg_loc))
        return msg_elem.text
