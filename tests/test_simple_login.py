# test_simple_login.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_saucedemo_login():
    # 启动Edge浏览器
    #Chrome浏览器相对慢很多默认会去**谷歌 github**校验 / 下载驱动，国内网络会卡住、长时间超时等待
    print("====开始启动Edge浏览器====")
    driver = webdriver.Edge()
    print("====浏览器启动成功====")
    driver.maximize_window()
    print("====窗口最大化====")
    driver.get("https://www.saucedemo.com")
    print("====网页加载完成====")
    # 显式等待，最长等待10秒加载元素
    wait = WebDriverWait(driver, 10)
    print("====创建等待对象====")
    # 输入用户名
    username_input = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    username_input.send_keys("standard_user")
    print("====输入用户名====")
    # 输入密码
    pwd_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
    pwd_input.send_keys("secret_sauce")
    print("====输入密码====")
    # 点击登录按钮
    login_btn = wait.until(EC.presence_of_element_located((By.ID, "login-button")))
    login_btn.click()
    print("====点击登录====")
    # 断言登录成功：页面出现Products标题
    title_text = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "title"))).text
    assert title_text == "Products"
    print("====断言成功！====")
    # 关闭浏览器
    driver.quit()
