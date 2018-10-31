# coding=utf-8
import time
import threading
from biz import easymoney_yaowen
from biz import easymoney_all
def start_easymoney_yaowen():
    print u"东方财经要闻 开始"
    # 调用今日头条热点的爬虫，实例化今日头条热点的爬虫类，将其编程对象，赋值给这个变量
    yw = easymoney_yaowen.easymoney_yaowen_biz()
    # 调用今日头条热点对象的getMain()方法，进行爬取操作
    yw.getMain()
    print (u"东方财经要闻 爬取完毕")
    # 主线程休眠
def start_easymoney_all():
    print u"东方财经其他 开始"
    # 调用今日头条热点的爬虫，实例化今日头条热点的爬虫类，将其编程对象，赋值给这个变量
    em = easymoney_all.easymoney_all_biz()
    # 调用今日头条热点对象的getMain()方法，进行爬取操作
    em.getMain()
    print (u"东方财经其他 爬取完毕")
# 线程池
# threads = []
# # 腾讯旅游线程
# t1 = threading.Thread(target=start_tencent_ly())
# threads.append(t1)
# # 腾讯体育线程
# t2 = threading.Thread(target=start_tencent_sports())
# threads.append(t2)
# 启动线程
if __name__ == '__main__':
    # for t in threads:
    #     if t.isAlive() == False:
    #         t.start()
    # start_easymoney_yaowen()
    start_easymoney_all()