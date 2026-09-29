import os
from datetime import datetime

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.edge.options import Options

# 项目公共模块导入
from common.logger import log, logger
from api.api_pages.login_api import LoginApi
from api.api_pages.user_info_api import UserInfoApi


# ========== UI浏览器fixture ==========
@pytest.fixture(scope="function")
def driver():
    # 配置Edge浏览器参数
    log.info("===== 开始初始化Edge浏览器 =====")
    edge_options = Options()
    edge_options.add_argument("--disable-features=RendererCodeIntegrity")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    # 解决renderer超时崩溃
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--no-sandbox")
    # 无头模式（CI环境用）
    # edge_options.add_argument("--headless=new")

    driver = webdriver.Edge(options=edge_options)
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(20)
    log.info("Edge浏览器启动成功，窗口最大化")

    yield driver

    # 用例执行完毕，关闭浏览器
    try:
        driver.quit()
        log.info("浏览器正常关闭")
    except Exception as e:
        log.error(f"关闭浏览器发生异常: {e}")


# ========== 截图目录配置 ==========
_base_dir = os.path.dirname(os.path.abspath(__file__))
_screenshot_dir = os.path.join(_base_dir, "screenshots")
if not os.path.exists(_screenshot_dir):
    os.makedirs(_screenshot_dir)

_log_dir = os.path.join(_base_dir, "logs")
if not os.path.exists(_log_dir):
    os.makedirs(_log_dir)


# ========== 用例失败自动截图/捕获接口报文钩子 ==========
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """pytest内置钩子：用例执行结束后自动触发"""
    outcome = yield
    rep = outcome.get_result()

    # 只在用例【执行阶段失败】时处理
    if rep.when == "call" and rep.failed:
        try:
            # 1. UI用例：有driver，自动截图并嵌入Allure报告
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(
                    _screenshot_dir,
                    f"{item.nodeid.replace('::', '_')}_{timestamp}.png"
                )
                driver.save_screenshot(save_path)
                logger.info(f"【失败截图已保存】{save_path}")

                # 截图嵌入Allure报告
                with open(save_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="用例失败截图",
                        attachment_type=allure.attachment_type.PNG
                    )

            # 2. 接口用例：读取挂载在item上的resp，自动保存失败报文
            else:
                if hasattr(item, "resp"):
                    resp = item.resp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    report_content = (
                        f"请求url：{resp.url}\n"
                        f"请求method：{resp.request.method}\n"
                        f"状态码：{resp.status_code}\n"
                        f"请求体：{resp.request.body}\n"
                        f"响应内容：{resp.text}"
                    )
                    report_name = f"api_fail_{item.nodeid.replace('::', '_')}_{timestamp}.txt"
                    report_path = os.path.join(_log_dir, report_name)

                    # 保存报文到本地日志文件
                    with open(report_path, "w", encoding="utf-8") as f:
                        f.write(report_content)

                    # 报文嵌入Allure报告
                    allure.attach(
                        report_content,
                        name="接口失败报文",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    logger.info(f"接口失败报文保存到：{report_path}")

        except Exception as e:
            logger.error(f"失败信息捕获异常：{str(e)}")


# ========== UI预登录fixture ==========
@pytest.fixture
def logged_in_driver(driver):
    """前置：直接完成登录，返回已登录浏览器对象"""
    from pages.login_page import LoginPage
    log.info("【前置fixture】执行预登录操作")
    login = LoginPage(driver)
    login.driver.get("https://www.saucedemo.com/")
    login.enter_username("standard_user")
    login.enter_password("secret_sauce")
    login.click_login()
    log.info("预登录完成")

    yield driver


# ========== 接口自动登录fixture ==========
@pytest.fixture(scope="session")
def logged_in_user_api():
    """
    session级别：只登录一次，返回携带token的user_api对象
    """
    logger.info("【fixture前置】自动执行登录接口")
    login_api = LoginApi()
    resp = login_api.login(username="test",password="123456")
    token = "abcdefg123456789token"
    login_api.save_token(token)
    user_api = UserInfoApi()
    user_api.token = login_api.token
    logger.info("【fixture】登录完成，token已绑定到接口对象")

    yield user_api

    logger.info("【fixture后置】当前接口用例执行完成")

# ===================== ✅【新增：pytest命令行参数 --env】 =====================
def pytest_addoption(parser):
    """注册命令行参数 --env，可选 dev/test，默认读取yaml里的env配置"""
    parser.addoption(
        "--env",
        action="store",
        default=None,
        choices=["dev", "test"],
        help="指定运行环境：dev / test，不传就读取config.yaml默认env"
    )

@pytest.fixture(scope="session", autouse=True)
def set_global_env(request):
    """✅【新增】自动加载环境，存入全局变量"""
    import builtins
    # 获取命令行传入的env
    cli_env = request.config.getoption("--env")
    builtins.GLOBAL_ENV = cli_env
    logger.info(f"【全局环境参数】命令行传入env = {builtins.GLOBAL_ENV}")


# ===================== ✅【新增：复用现有GoodsApi的临时商品fixture】 =====================
@pytest.fixture(scope="function")
def temp_goods_fixture(db_client):
    """
    setup：调用接口新增商品 + 插入MySQL
    yield：把商品id传给测试用例
    teardown：自动删除商品+删除数据库记录
    """
    from api.api_pages.goods_api import GoodsApi
    goods_api = GoodsApi()
    goods_name = "自动化临时商品"
    price = 66.6
    # --------1.前置：调用你已有的新增商品接口--------
    logger.info("【setup前置】创建临时商品测试数据")
    # 调用新增商品接口，这里参数可以自定义
    add_resp = goods_api.add_goods(goods_name=goods_name, price=price)
    # 真实业务：goods_id = add_resp.json()["goods_id"]
    goods_id = 10002
    logger.info(f"临时商品创建成功，goods_id: {goods_id}")
    # 2.把这条商品写入MySQL
    insert_sql = """
    INSERT INTO goods(goods_name, price)VALUES(%s, %s)
    """
    db_client.execute_sql(insert_sql, args=(goods_name, price))
    logger.info("【DB】商品数据插入mysql成功")
    # 传给测试用例
    yield goods_id, goods_name, price
    # 3、后置清理：接口删除 + 数据库删除
    logger.info("【teardown后置】清理临时商品")
    goods_api.delete_goods(goods_id=goods_id)
    # 删除数据库数据
    del_sql = "DELETE FROM goods WHERE goods_name=%s AND price=%s"
    db_client.execute_sql(del_sql, args=(goods_name, price))
    logger.info("【DB】数据库临时商品已删除")



@pytest.fixture(scope="session")
def db_client():
    """数据库连接fixture，整个测试只创建一次连接"""
    import builtins
    from common.db_util import DBUtil
    env = builtins.GLOBAL_ENV
    db = DBUtil(env=env)
    db.connect()
    yield db
    db.close()
