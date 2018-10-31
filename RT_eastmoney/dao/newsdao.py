# coding=utf-8
from utilz import dbmysql, util

'''
dao层侧重对数据表的操作，数据表的增删查改操作
'''
# 根据url判断数据库中是否已存在，
def getUrlData(url):
    try:
        url = url.encode('utf-8')
        # sql语句，返回第一条数据，即返回的count
        sql = "SELECT count(1) FROM fy_ft_news_eastmoney WHERE news_url='%s';" % (url)
        # 调用dbmysql执行查询方法
        rs = dbmysql.first(sql)
        # 如果数据表中存在url，返回true，不存在的话，返回false，故障情况下，返回None
        if rs[0] > 0:
            return True
        else:
            return False
    except Exception, ex:
        print (ex.message)
        return None
def getAll(var):
    return var.replace(":", "：").replace("'", "‘").encode('utf-8')
# 插入data
def insertData(flag01, web_from, flag02, title, news_from, news_url, news_text, image_url, create_time, looked,
               comment,forward,good_num,ts,pt):
    try:
        # 获取UUID的值
        # logId = util.getUUID().encode('utf-8')
        # 对获取过来的数据，进行简单处理操作，比如，获取的数据中存在  ‘'’，那么在执行sql语句的过程中必然会出错
        # body = body.replace(":", "：").replace("'", "‘").encode('utf-8')
        flag01 = getAll(flag01)
        web_from = getAll(web_from)
        flag02 = getAll(flag02)
        title = getAll(title)
        news_from = getAll(news_from)
        news_url = getAll(news_url)
        news_text = getAll(news_text)
        image_url = getAll(image_url)
        create_time = getAll(create_time)
        looked = looked
        comment = comment
        forward = forward
        good_num = good_num
        ts = ts
        pt = pt
        # sql语句，插入到mysql当中
        sql = "INSERT INTO fy_ft_news_eastmoney(flag01,web_from,flag02,title,news_from,news_url,news_text,image_url,create_time,looked,comment,forward,good_num,ts,pt) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
            flag01, web_from, flag02, title, news_from, news_url, news_text, image_url, create_time, looked, comment,
            forward, good_num, ts, pt)
        # 执行sql语句
        rs = dbmysql.query(sql)
        if rs == True:
            print 'ok'
            return True
        else:
            return False
    except Exception, ex:
        print (ex.message)
        return None

# 查询全部
def getType():
    try:
        # 查询语句，查询news表中的所有数据
        sql = "select * from fy_ft_news_eastmoney order by insertTime;"
        # 执行sql语句，返回所有数据
        rs = dbmysql.fetchall(sql)
        if rs:
            return rs
    except Exception, ex:
        print (ex.message)
        return None
