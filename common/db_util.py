import pymysql
from common.get_env_config import get_env_config
from common.logger import logger

class DBUtil:
    def __init__(self, env):
        # 读取器yaml里面对应环境的数据库配置
        self.db_conf = get_env_config(key="db_config", env=env)
        self.conn = None
        self.cursor = None


    def connect(self):
        """建立数据库连接"""
        try:
            self.conn = pymysql.connect(
                host=self.db_conf["host"],
                port=self.db_conf["port"],
                user=self.db_conf["user"],
                password=self.db_conf["password"],
                database=self.db_conf["database"],
                charset=self.db_conf["charset"]
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            logger.info(f"MYSQL数据库连接成功")
        except Exception as e:
            logger.error(f"数据库连接失败")
            raise e


    def query_one(self, sql, args=None):
        """查询单条记录"""
        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    def execute_sql(self, sql, args=None):
        """执行增删改查"""
        self.cursor.execute(sql, args)
        self.conn.commit()

    def close(self):
        """关闭游标和连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("数据库连接关闭")


