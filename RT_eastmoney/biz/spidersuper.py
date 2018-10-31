# coding=utf-8
from dao import newsdao

#父类
# 提取共有的方法放到父类当中
class spidersuper():
    def __init__(self):
        #定义三个类变量，在调用框架的时候，可以对类变量根据需求进行重新定义
        self.flag01 = ''
        self.web_from = ''
        self.flag02 = ''
        self.title = ''
        self.news_from = ''
        self.news_url = ''
        self.news_text = ''
        self.image_url = ''
        self.create_time = ''
        self.looked = ''
        self.comment = ''
        self.forward = ''
        self.good_num = ''
        self.ts = ''
        self.pt = ''
    #析构方法，通知python解释器进行垃圾回收
    def __del__(self):
        del (self)
    #提取的共性方法，判断url是否存在
    def getDataByUrl(self):
        #调用dao中的方法，根据返回值进行判断，如果返回值为False，则表示数据表中不存在此url，可以将此url数据插入到数据表中
        #rs==False可以插入到数据表中
        #rs==None，表示故障
        #rs为其他的值（也就是True）表示数据表中已经存在此数据，不再进行插入操作
        rs = newsdao.getUrlData(url=self.news_url)
        if rs == False:
            return False
        elif rs is None:
            return 1
        else:
            return 2
    #插入数据表
    def insertData(self):
        #如果rs的返回值为False的时候，表示此url地址不在数据表中存在，即可以插入数据
        rs=self.getDataByUrl()
        if rs == False:
            newsdao.insertData(
                flag01=self.flag01,
                web_from=self.web_from,
                flag02=self.flag02,
                title=self.title,
                news_from=self.news_from,
                news_url=self.news_url,
                news_text=self.news_text,
                image_url=self.image_url,
                create_time=self.create_time,
                looked=self.looked,
                comment=self.comment,
                good_num=self.good_num,
                ts=self.ts,
                pt=self.pt,
                forward=self.forward
            )