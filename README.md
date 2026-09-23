# Selenium+Pytest UI自动化测试Demo
> 软件测试作品集项目，基于Page Object Model(POM)设计模式，针对SauceDemo演示电商网站做UI自动化。

## 技术栈
- Python + Pytest 测试框架
- Selenium WebDriver 页面自动化
- YAML 管理测试数据，数据与代码分离
- 自动截图：用例失败自动截图保存到screenshots目录
- HTML测试报告输出

## 项目结构
selenium-ui-demo
├── common/                # 公共工具类
│   └── read_data.py       # yaml 读取工具
├── data/                  # 测试数据 yaml 文件
│   ├── login_data.yaml
│   ├── inventory_data.yaml
│   ├── cart_data.yaml
│   └── checkout_data.yaml
├── pages/                 # POM 页面层
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                 # 测试用例
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── screenshots/           # 失败用例截图
├── report/                # html 测试报告
├── logs/                  # 日志
├── requirements.txt       # 依赖清单
└── README.md

## 覆盖用例
1. 登录模块：正常登录 / 账号密码错误反向用例
2. 商品页：商品加入购物车
3. 购物车：跳转结算页面
4. 结算模块：
   - 正向：完整信息提交，下单成功
   - 反向：空信息提交，校验错误提示

## 运行步骤
1. 创建虚拟环境
`python -m venv venv`
2. 激活虚拟环境
windows: `venv\Scripts\activate`
3. 安装依赖
`pip install -r requirements.txt`
4. 执行全部用例
`pytest tests/ -v -s --html=report/report.html`

## 项目亮点
1. POM分层，页面元素、操作、测试用例解耦，维护性强
2. 测试数据写在yaml，不用改动代码即可修改数据
3. 用例失败自动截图，方便定位问题
4. 支持生成HTML可视化测试报告
