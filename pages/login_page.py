from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 新增导入日志
from common.logger import log


class LoginPage:
    # 元素定位器
    username_loc = (By.ID, "user-name")
    password_loc = (By.ID, "password")
    login_btn_loc = (By.ID, "login-button")
    error_msg_loc = (By.CLASS_NAME, "error-message-container")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        log.info("实例化登录页面对象")

    def open_url(self):
        """打开登录页面"""
        log.info("访问SauceDemo登录页面")
        self.driver.get("https://www.saucedemo.com/")

    def enter_username(self, username):
        """输入用户名"""
        log.info(f"输入用户名：{username}")
        elem = self.wait.until(EC.element_to_be_clickable(self.username_loc))
        elem.clear()
        elem.send_keys(username)

    def enter_password(self, password):
        """输入密码"""
        log.info(f"输入密码：{password}")
        elem = self.wait.until(EC.element_to_be_clickable(self.password_loc))
        elem.clear()
        elem.send_keys(password)

    def click_login(self):
        """点击登录按钮"""
        log.info("点击登录按钮")
        self.wait.until(EC.element_to_be_clickable(self.login_btn_loc)).click()

    def login(self, username, password):
        """完整登录操作"""
        log.info(f"执行完整登录流程，账号：{username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_msg(self):
        """获取登录失败的错误提示"""
        elem = self.wait.until(EC.presence_of_element_located(self.error_msg_loc))
        error_text = elem.text
        log.warning(f"登录获取到错误提示: {error_text}")
        return error_text
