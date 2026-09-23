import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options

@pytest.fixture(scope="function")
def driver():
    # 配置Edge浏览器参数
    edge_options = Options()
    edge_options.add_argument("--disable-features=RendererCodeIntegrity")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    # 可选：取消下面注释就是无头模式，后台运行不弹出浏览器
    # edge_options.add_argument("--headless=new")
    driver = webdriver.Edge(options=edge_options)
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    yield driver
    # 用例执行完毕，关闭浏览器
    try:
        driver.quit()
    except Exception:
        pass


# ========== 用例失败自动截图钩子 ==========
import os
from datetime import datetime

# 截图保存目录：项目根目录/screenshots
_base_dir = os.path.dirname(os.path.abspath(__file__))
_screenshot_dir = os.path.join(_base_dir, "screenshots")
if not os.path.exists(_screenshot_dir):
    os.makedirs(_screenshot_dir)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """pytest内置钩子：用例执行结束后自动触发"""
    outcome = yield
    rep = outcome.get_result()

    # 只在用例【执行阶段失败】时截图
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs["driver"]
            # 时间戳命名，防止覆盖
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            case_name = item.name.replace("/", "_").replace("\\", "_").replace("[", "_").replace("]", "_")
            file_name = f"fail_{case_name}_{timestamp}.png"
            screenshot_path = os.path.join(_screenshot_dir, file_name)
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 失败截图已保存：{screenshot_path}")
        except Exception as e:
            print(f"\n 截图失败：{e}")

@pytest.fixture
def logged_in_driver(driver):
    # 前置：直接完成登录，返回已登录浏览器对象
    from pages.login_page import LoginPage
    login = LoginPage(driver)
    login.driver.get("https://www.saucedemo.com/")
    login.enter_username("standard_user")
    login.enter_password("secret_sauce")
    login.click_login()
    yield driver
    # yield之后，用例执行完自动关闭
