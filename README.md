# Selenium+Pytest UI自动化测试框架
> 基于PO(Page Object)模式实现SauceDemo电商网站UI自动化

## 项目介绍
本项目基于`Selenium + Pytest`搭建UI自动化测试框架，测试目标网站：https://www.saucedemo.com
覆盖电商核心业务流程：登录、商品浏览、加入购物车、删除购物车商品、订单结算；同时包含异常场景测试。

## 框架特性
1. PO 页面对象模型：页面元素和业务操作分离，维护简单
2. YAML数据驱动：测试数据和代码解耦，方便新增用例
3. pytest标记用例：支持冒烟测试/异常测试/全量回归，按需执行
4. 失败自动截图：用例执行失败自动保存截图，方便定位bug
5. 日志模块：执行过程自动打印日志，便于排查问题
6. 失败重跑：pytest-rerunfailures，解决UI自动化偶现不稳定问题
7. 显式等待WebDriverWait，规避页面加载时序问题

##  项目目录说明
selenium-ui-demo/
├── common/               # 公共工具类
│   ├── logger.py         # 日志封装
│   └── read_data.py     # yaml读取工具
├── data/                 # yaml测试数据
├── pages/                # PO页面层
├── tests/                # 测试用例层
├── logs/                 # 运行日志（.gitignore忽略）
├── screenshots/          # 失败截图（.gitignore忽略）
├── report/               # html测试报告（.gitignore忽略）
├── conftest.py           # pytest全局配置、fixture、失败截图钩子
├── pytest.ini            # pytest标记配置
├── requirements.txt      # 项目依赖包
├── .gitignore            # git忽略不需要上传的文件
└── README.md             # 项目说明文档

##  环境依赖
- Python 3.9+
- Selenium
- pytest
- pytest-rerunfailures
- pyyaml
- pytest-html

##  运行方式
1. 克隆项目
```bash
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
# 执行并生成html报告
pytest -v -s --html=reports/report.html
# 用例失败自动重跑2次，每次间隔1秒
pytest -v -s --reruns 2 --reruns-delay 1

## 覆盖测试场景
### 正向用例（smoke）
- 正常账号密码登录
- 商品列表页面校验
- 添加商品到购物车
- 购物车删除商品
- 完整下单结算流程

### 异常用例（negative）
- 用户名为空登录
- 密码为空登录
- 账号正确，密码错误
- 结算页面不填信息直接提交

## 项目功能亮点
1. PO 分层设计：页面元素定位、页面操作 和 测试用例代码解耦，维护性强
2. YAML 数据驱动：多组测试数据写在 data 目录 yaml 文件，无需改动代码新增用例
3. 失败自动截图：用例执行失败自动保存截图到 screenshots
4. 失败自动重试：UI 自动化不稳定场景自动重跑，提升稳定性
5. 用例标签化：区分冒烟测试、反向异常测试，支持按需执行子集用例
6. 独立日志目录：logs 文件夹记录执行过程，方便排查

## 迭代计划
1. 完善 common 模块，封装全局 logging 日志
2. 补齐结算页 test_checkout.py 冒烟标记 @pytest.mark.smoke
3. 浏览器配置抽离，支持一键切换 Edge / Chrome
4. （进阶）接入 Allure 测试报告，替换 html 简易报告