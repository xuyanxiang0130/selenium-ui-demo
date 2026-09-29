# Pytest UI+接口一体化自动化测试框架
> 练习项目：Pytest + Selenium + Requests + Mysql + Allure

## 框架特性
- WebUI：Selenium + PO页面对象模式，显式等待，用例失败自动截图保存
- 接口自动化：BaseApi基类封装，统一请求、token鉴权、请求日志输出
- 数据驱动：YAML管理测试用例与多环境(dev/test)配置
- 数据库：pymysql封装DB工具，**接口+MySQL双重断言**，校验业务数据落库正确性
- 测试数据：pytest‑fixture完成前置造数据，teardown自动清理MySQL脏数据，保证每条用例独立运行
- 报告日志：Allure可视化报告，全局日志记录接口请求、响应、数据库操作
- 用例管理：mark标签 `smoke / regression / negative / ui / api`，支持筛选执行、失败重跑

## 技术栈
Python3.9 | Pytest | Selenium | Requests | PyMySQL | PyYAML | Allure‑pytest

## 📂项目目录说明
selenium-ui-demo/
├── api/                     # 接口自动化模块
│   ├── __init__.py
│   ├── api_data/            # 接口 yaml 测试数据
│   │   ├── goods_api_data.yaml
│   │   └── login_api_data.yaml
│   ├── api_pages/           # 接口 PO 层：封装接口地址、请求方法
│   │   ├── base_api.py      # 接口基类BaseApi
│   │   ├── goods_api.py
│   │   ├── login_api.py
│   │   └── user_info_api.py
│   └── test_api/            # 接口测试用例
│       ├── test_goods_api.py
│       ├── test_login_api.py
│       └── test_user_info_api.py
├── common/                  # 公共工具类（UI、接口共用）
│   ├── logger.py            # 全局日志封装
│   ├── read_data.py         # yaml 读取工具
│   ├── get_env_config.py    # 多环境配置读取工具
│   ├── db_util.py           # mysql数据库操作工具类
│   └── assert_util.py        # 通用断言工具
├── data/                    # 配置文件 & UI自动化yaml测试数据
│   ├── config.yaml          # 多环境、数据库账号配置
│   ├── cart_data.yaml
│   ├── checkout_data.yaml
│   ├── inventory_data.yaml
│   ├── login_data.yaml
│   └── test_data.yaml
├── pages/                   # UI 页面 PO 层，封装页面元素与业务操作
│   ├── __init__.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── inventory_page.py
│   └── login_page.py
├── tests/                   # UI 自动化测试用例
│   ├── __init__.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   ├── test_inventory.py
│   ├── test_login.py
│   └── test_simple_login.py
├── logs/                    # 运行日志（.gitignore 忽略）
├── report/                  # html 测试报告存放目录（.gitignore 忽略）
│   └── report.html
├── screenshots/             # UI 用例失败截图目录（.gitignore 忽略）
├── venv/                    # Python 虚拟环境，不上传 git（.gitignore 忽略）
├── .gitignore               # git 忽略配置文件
├── conftest.py              # pytest全局fixture、数据库fixture、浏览器配置、失败截图钩子
├── pytest.ini               # pytest 标记、全局配置
├── requirements.txt         # 项目第三方依赖清单
└── README.md                # 项目说明文档
```

## 运行步骤
```bash
# 1、创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 2、安装依赖
pip install -r requirements.txt

# 3、准备数据库
# 执行下面SQL脚本创建 test_auto库、goods商品表，修改 data/config.yaml 中mysql账号密码
"""
CREATE DATABASE IF NOT EXISTS test_auto DEFAULT CHARACTER SET utf8mb4;
USE test_auto;
CREATE TABLE IF NOT EXISTS goods(
    id INT PRIMARY KEY AUTO_INCREMENT,
    goods_name VARCHAR(100),
    price DECIMAL(10,2),
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

# ---------------------- 接口自动化用例执行 ----------------------
# 执行全部接口用例
pytest api/test_api/ -v -s --alluredir=allure-results

# 只跑接口冒烟用例
pytest api/test_api/ -m "api and smoke" -v -s --alluredir=allure-results

# ---------------------- Web UI自动化用例执行 ----------------------
# 执行全部UI自动化用例（UI用例直接放在tests下，不是tests/test_ui）
pytest tests/ -v -s --alluredir=allure-results

# 只跑UI冒烟用例
pytest tests/ -m "ui and smoke" -v -s --alluredir=allure-results

# ---------------------- 混合执行 ----------------------
# 同时执行UI+接口全部冒烟用例
pytest -m "smoke" -v -s --alluredir=allure-results

# 4、生成并打开allure报告
allure generate allure-results -o allure-report --clean
allure open allure-report
```

> 
> 1. UI自动化会唤起浏览器，请提前配置Edge驱动；
> 2. 修改`data/config.yaml`配置数据库host/user/password/database；
> 3. 接口使用 httpbin 模拟后端服务，不需要启动本地后端服务。

## 覆盖测试场景
### Web UI 自动化
#### 正向用例（smoke）
- 正常账号密码登录
- 商品列表页面校验
- 添加商品到购物车
- 购物车删除商品

#### 异常用例（negative）
- 用户名为空登录
- 密码为空登录
- 账号正确，密码错误

### 接口自动化（httpbin 模拟接口）
#### 接口测试用例（api 标记）
- POST 模拟登录接口，YAML 数据驱动（正常账号、空用户名）
- GET 商品列表分页查询接口，增加MySQL数据库断言
- 接口串联（接口关联）：登录模拟获取 token，携带 Token 鉴权访问用户信息接口
- pytest‑fixture自动构造商品测试数据，执行完成自动清理脏数据

## 项目功能亮点
1. PO分层设计：页面元素定位、页面操作 和 测试用例代码解耦，后期维护只需要修改page层，不改动业务用例。
2. YAML数据驱动：多组测试数据维护在yaml文件，新增测试场景无需修改业务代码。
3. 失败自动截图：UI用例执行失败自动保存截图到`screenshots`目录，截图嵌入Allure报告，便于缺陷定位。
4. 失败自动重试：UI自动化受页面加载波动影响，使用`pytest‑rerunfailures`实现失败重跑，提升脚本稳定性。
5. 用例标签化：区分冒烟测试`smoke`、回归`regression`、反向异常`negative`、ui/api模块标签，可以按需执行子集用例。
6. 数据库双重校验：封装DB工具类，除接口响应断言外，查询MySQL校验数据落库；fixture自动生成&删除临时测试数据，不污染测试环境。
7. 独立日志目录：logs文件夹记录请求响应、数据库操作日志，方便脚本调试排查问题。
8. 公共组件复用：日志、yaml读取、数据库工具，UI自动化与接口自动化共用，减少重复开发。
9. 多环境支持：通过`config.yaml`维护dev/test两套环境配置，可灵活切换运行环境。

## 后续迭代计划
1. 完善common模块，统一日志输出格式，优化异常捕获。
2. 补齐`test_checkout.py`用例，添加`@pytest.mark.smoke`冒烟标记。
3. 将浏览器参数抽离配置文件，支持一键切换 Chrome / Edge 浏览器。
4. 优化数据库fixture兜底逻辑：如果teardown删除SQL异常，增加告警日志，避免脏数据残留。
5. 增加通用断言工具封装，统一接口、数据库字段比对逻辑。


