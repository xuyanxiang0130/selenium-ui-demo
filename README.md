# 自动化测试项目（UI+接口一体化框架）
> 基于Python + Pytest搭建，**一套框架同时支持Web UI自动化、接口自动化，采用PO设计模式

## 项目介绍
本项目基于`Selenium + Pytest`搭建UI自动化测试框架，测试目标网站：https://www.saucedemo.com
覆盖电商核心业务流程：登录、商品浏览、加入购物车、删除购物车商品；同时包含各类异常场景测试。
同时集成Requests接口自动化模块，采用接口PO模式，基于httpbin模拟接口完成接口测试，实现登录鉴权、接口串联、数据驱动，公共工具（日志、yaml读取）UI与接口复用。

## 框架特性
1. PO 页面对象模型：页面元素和业务操作分离，维护简单
2. YAML数据驱动：测试数据和代码解耦，方便新增用例，UI、接口共用yaml解析工具
3. pytest标记用例：支持冒烟测试/异常测试/接口测试，按需执行
4. 失败自动截图：UI用例执行失败自动保存截图，方便定位bug
5. 日志模块：执行过程自动打印日志，UI、接口共用日志，便于排查问题
6. 失败重跑：pytest-rerunfailures，解决UI自动化偶现不稳定问题
7. 显式等待WebDriverWait，规避页面加载时序问题
8. 接口关联能力：支持登录获取token，携带token完成鉴权接口调用

##  项目目录说明
selenium-ui-demo/
├── api/                     # 接口自动化模块
│   ├── **init**.py
│   ├── api_data/            # 接口 yaml 测试数据
│   │   ├── goods_api_data.yaml
│   │   └── login_api_data.yaml
│   ├── api_pages/           # 接口 PO 层：封装接口地址、请求方法
│   │   ├── goods_api.py
│   │   ├── login_api.py
│   │   └── user_info_api.py
│   └── test_api/            # 接口测试用例
│       ├── test_goods_api.py
│       ├── test_login_api.py
│       └── test_user_info_api.py
├── common/                  # 公共工具类（UI、接口共用）
│   ├── logger.py            # 日志封装
│   └── read_data.py         # yaml 读取工具
├── data/                    # UI 自动化 yaml 测试数据
│   ├── cart_data.yaml
│   ├── checkout_data.yaml
│   ├── inventory_data.yaml
│   ├── login_data.yaml
│   └── test_data.yaml
├── pages/                   # UI 页面 PO 层，封装页面元素与业务操作
│   ├── **init**.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── inventory_page.py
│   └── login_page.py
├── tests/                   # UI 自动化测试用例
│   ├── **init**.py
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
├── conftest.py              # pytest 全局 fixture、浏览器配置、失败截图钩子
├── pytest.ini               # pytest 标记、全局配置
├── requirements.txt         # 项目第三方依赖清单
└── README.md                # 项目说明文档

##  环境依赖
- Python 3.9+
- Selenium
- pytest
- pytest-rerunfailures
- pyyaml
- pytest-html
- requests

##  运行方式
1. 克隆项目
git clone xxx你的github仓库地址
cd selenium-ui-demo

2. 创建虚拟环境
python -m venv venv

# windows激活虚拟环境
venv\Scripts\activate

3. 安装依赖
pip install -r requirements.txt
 
4.用例命令
# 冒烟测试（核心正向业务）
pytest -m smoke -v -s

# 异常场景测试
pytest -m negative -v -s

# 全量回归所有用例
pytest -v -s

# 执行接口自动化用例
pytest api/test_api/ -m api -v -s

# UI+接口，全量回归所有用例
pytest -v -s

# 执行并生成html报告
pytest -v -s --html=reports/report.html

# 用例失败自动重跑2次，每次间隔1秒
pytest -v -s --reruns 2 --reruns-delay 1

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
- GET 商品列表分页查询接口
- 接口串联（接口关联）：登录模拟获取 token，携带 Token 鉴权访问用户信息接口

## 项目功能亮点
1. PO 分层设计：页面元素定位、页面操作 和 测试用例代码解耦，维护性强
2. YAML 数据驱动：多组测试数据写在 data 目录 yaml 文件，无需改动代码新增用例
3. 失败自动截图：用例执行失败自动保存截图到 screenshots
4. 失败自动重试：UI 自动化不稳定场景自动重跑，提升稳定性
5. 用例标签化：区分冒烟测试、反向异常测试，支持按需执行子集用例
6. 独立日志目录：logs 文件夹记录执行过程，方便排查
7. 公共组件复用：日志、yaml 读取工具，UI 自动化与接口自动化共用，减少重复开发

## 迭代计划
1. 完善 common 模块，封装全局 logging 日志
2. 补齐结算页 test_checkout.py 冒烟标记 @pytest.mark.smoke
3. 浏览器配置抽离，支持一键切换 Edge / Chrome
4. （进阶）接入 Allure 测试报告，替换 html 简易报告