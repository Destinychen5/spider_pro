# coding=utf-8
from utilz import util
import time,random
from lxml import etree
from biz import spidersuper
import os
import datetime
# 腾讯爬虫
# 继承父类
class easymoney_yaowen_biz(spidersuper.spidersuper):
    def __init__(self):
        # 启动父类的所有方法和变量
        spidersuper.spidersuper.__init__(self)
    # 腾讯爬虫的主程序入口
    def getMain(self):
        try:
            part_list = ['cgnjj','cgjjj','czqyw','cgsxw']
            for part in part_list:
                for num in xrange(1,26):
                    self.__getsingle(part,num)
        except Exception, ex:
            print ex.message
    def __getsingle(self,part,num):
        try:
            user_agent_lists = [
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0",
                "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"
            ]
            hheaders = {
                "User-Agent": random.choice(user_agent_lists),
                "Referer": "http://finance.eastmoney.com/news/cgnjj.html"
            }
            if num == 1:
                url = 'http://finance.eastmoney.com/news/%s'%part +'.html'
            else:
                url = 'http://finance.eastmoney.com/news/%s_%s'%(part,num) +'.html'
            r_content = util.get(url=url, header=hheaders)
            if r_content["issuccess"] != 1:
                return None
            d_html = r_content["message"]
            tree = etree.HTML(d_html)
            data_list = tree.xpath('//ul[@id="newsListContent"]/li')
            for data in data_list:
                self.title = data.xpath('./div/p/a/text()')[0].replace('\r','').replace('\n','').replace(' ','')
                self.news_url= data.xpath('./div/p/a/@href')[0]
                self.__getDetails(self.news_url)
                self.flag01 = "财经"
                self.web_from = "东方财经"
                self.flag02 = "东方财经-财经要闻"
                self.pt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                self.ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.insertData()
                print self.create_time
                self.news_text = ''
                self.image_url = ''
        except Exception, ex:
            print ex.message
    def __getDetails(self,urls):
        try:
            # 爬取部分
            res = util.get(url=urls)
            if res["issuccess"] != True:
                return None
            htmls = res["message"]
            tree = etree.HTML(htmls)
            try:
                self.comment = tree.xpath('//span[@class="num ml5"]/text()')[0]
            except Exception:
                self.comment = 0
            self.create_time = tree.xpath('//div[@class="time"]/text()')[0]
            self.news_from = tree.xpath('//div[@class="source data-source"]/@data-source')[0].encode('utf-8')
            news_text = tree.xpath('//div[@id="ContentBody"]//p/text()')
            try:
                review = tree.xpath('//div[@class="b-review"]/text()')[0]
                if len(review):
                    news_text.insert(0,review)
                else:
                    return None
            except Exception as ex:
                news_text.insert(0,'')
            news_str = '\n'.join(news_text)
            self.news_text = util.getNoHtmlBody(news_str)
            try:
                img_list = tree.xpath('//div[@id="ContentBody"]//img/@src')
                if len(img_list)>0:
                    path_list = []
                    for img in img_list:
                        p = util.get(url=img)
                        if p["issuccess"] != 1:
                            return None
                        html = p["message"]
                        if html:
                              num = util.getUUID()
                              with open('./eastmoney/yaowen/%s.jpg' %num , 'wb') as f:
                                 f.write(html)
                                 paths = os.path.abspath('./eastmoney/yaowen/%s.jpg' % num)
                                 path_list.append(paths)
                        self.image_url = ','.join(path_list)
                else:
                    self.image_url = ''
            except Exception as ex:
                self.image_url=''
            self.looked = 0
            #转发量
            self.forward = 0
            #点赞量
            self.good_num = 0
        except Exception, ex:
            print ex.message
