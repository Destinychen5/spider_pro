# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import config

# 配置文件中读取连接串
DB_URI = config.DB.MYSQL_PROD
# pool_size连接池数量
# pool_recycle连接池中空闲时间超过设定时间后，进行释放
# echo输出日志
# create_engine 初始化数据库连接
engine = create_engine(DB_URI, echo=False, pool_size=50, pool_recycle=1800)


# 插入，修改，删除操作
def query(sql):
    # 创建DBSession类型:
    DB_Session = sessionmaker(bind=engine)
    # 创建session对象:
    DB = DB_Session()
    try:
        # 执行sql语句
        DB.execute(text(sql))
        DB.commit()
        return True
    except Exception, ex:
        print ("exec sql got error:%s" % (ex.message))
        DB.rollback()
        return False
    finally:
        DB.close()


# 查询第一条数据
def first(sql):
    # 创建DBSession类型:
    DB_Session = sessionmaker(bind=engine)
    # 创建session对象:
    DB = DB_Session()
    try:
        # 执行sql语句，.first  session对象返回第一条数据
        rs = DB.execute(text(sql)).first()
        DB.commit()
        return rs
    except Exception, ex:
        print ("exec sql got error:%s" % (ex.message))
        DB.rollback()
        return False
    finally:
        DB.close()
# 查询多条数据
def fetchall(sql):
    # 创建DBSession类型:
    DB_Session = sessionmaker(bind=engine)
    # 创建session对象:
    DB = DB_Session()
    try:
        # 执行sql语句,.fetchall  session对象返回全部数据
        rs = DB.execute(text(sql)).fetchall()
        DB.commit()
        return rs
    except Exception, ex:
        print ("exec sql got error:%s" % (ex.message))
        DB.rollback()
        return False
    finally:
        DB.close()
