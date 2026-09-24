from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.logger import log


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
        self.wait = WebDriverWait(driver, 10)
        log.info("实例化结算页面CheckoutPage对象")

    def fill_info(self, firstname, lastname, postal_code):
        """填写结算收货信息"""
        log.info(f"填写结算信息：名:{firstname},姓:{lastname},邮编:{postal_code}")
        self.wait.until(EC.element_to_be_clickable(self.first_name_loc)).send_keys(firstname)
        self.wait.until(EC.element_to_be_clickable(self.last_name_loc)).send_keys(lastname)
        self.wait.until(EC.element_to_be_clickable(self.postal_code_loc)).send_keys(postal_code)

    def click_continue(self):
        """点击continue按钮"""
        log.info("点击结算页面continue按钮")
        self.wait.until(EC.element_to_be_clickable(self.continue_btn_loc)).click()

    def click_finish(self):
        """点击finish完成下单"""
        log.info("点击finish按钮，提交订单")
        self.wait.until(EC.element_to_be_clickable(self.finish_btn_loc)).click()

    def get_complete_message(self):
        """获取下单成功提示文本"""
        log.info("获取订单完成提示文案")
        msg_elem = self.wait.until(EC.presence_of_element_located(self.complete_msg_loc))
        msg_text = msg_elem.text
        log.info(f"订单完成提示：{msg_text}")
        return msg_text
