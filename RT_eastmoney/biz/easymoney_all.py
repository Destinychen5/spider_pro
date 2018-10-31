# coding=utf-8
import sys
sys.path.append('/home/chenyanan/biz')
sys.path.append('/home/chenyanan/utilz')
from utilz import util
import time,random
from lxml import etree
from biz import spidersuper
import json
import os
import datetime
# 腾讯爬虫
# 继承父类
class easymoney_all_biz(spidersuper.spidersuper):
    def __init__(self):
        # 启动父类的所有方法和变量
        spidersuper.spidersuper.__init__(self)
    # 腾讯爬虫的主程序入口
    def getMain(self):
        try:
            part_list = [
                {'name':'zhibo','getlist':'zhiboall','page':70,'flag':'东方财经-股市直播'},
                {'name': 'kuaixun', 'getlist': '109', 'page': 50,'flag':'东方财经-财经快讯文章'},
                {'name': 'shangshigs', 'getlist': '103', 'page': 50,'flag':'东方财经-上市公司资讯'},
                {'name': 'gushi', 'getlist': '105', 'page': 50,'flag':'东方财经-全球股市资讯'},
                {'name': 'yanghang', 'getlist': '118,119,120,121,122,123,124', 'page': 50, 'flag': '东方财经-央行资讯'},
                {'name': 'shangpin', 'getlist': '106', 'page': 50,'flag':'东方财经-商品资讯'},
                {'name': 'waihui', 'getlist': '107', 'page': 50,'flag':'东方财经-外汇资讯'},
                {'name': 'zhaiquan', 'getlist': '108', 'page': 50,'flag':'东方财经-债券资讯'},
                {'name': 'jijin', 'getlist': '109', 'page': 50,'flag':'东方财经-基金资讯'},
            ]
            for part in part_list:
                if part['name']=='zhibo':
                    for num in xrange(1,24):
                        self.__getsingle(part,num)
                else:
                    for i in xrange(1,21):
                        self.__getsingle(part,i)
        except Exception, ex:
            print ex.message
    def __getsingle(self,part,num):
        try:
            #随机UA
            user_agent_lists = [
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/57.0",
                "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"
            ]
            hheaders = {
                "User-Agent": random.choice(user_agent_lists),
                "Referer": "http://kuaixun.eastmoney.com"
            }
            url = 'http://newsapi.eastmoney.com/kuaixun/v1/getlist_%s_ajaxResult_%s_%s_.html'%(part['getlist'],part['page'],num)
            r_content = util.get(url=url, header=hheaders)
            if r_content["issuccess"] != 1:
                return None
            d_html = r_content["message"]
            data_str = d_html.replace('var ajaxResult=','')
            data_json = json.loads(data_str)
            if not data_json['LivesList']:
                return None
            data_list = data_json['LivesList']
            for data in data_list:
                self.title = data['title']
                self.news_url= data['url_w']
                self.__getDetails(self.news_url,part)
                if self.news_text =="":
                    self.news_text = data["digest"]
                else:
                    self.news_text = ''
                self.flag01 = "财经"
                self.web_from = "东方财经"
                self.flag02 = part['flag']
                self.pt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                self.ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.insertData()
                print self.create_time
                self.news_text = ''
                self.image_url = ''
        except Exception, ex:
            print ex.message
    def __getDetails(self,urls,part):
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
            if '//data.eastmoney.com' in str(urls):
                self.create_time = tree.xpath('//div[@class="report-infos"]/span[2]/text()')[0].replace(' ','')
                news_text = tree.xpath('//div[@class="newsContent"]//p//text()')
                source = tree.xpath('//div[@class="report-infos"]/span[3]/text()')[0]
                self.news_from = source.replace('\r', '').replace('\n', '').replace(' ', '')
            else:
                self.create_time = tree.xpath('//div[@class="time"]/text()')[0].encode('utf-8')
                news_from = tree.xpath('//div[@class="source data-source"]/@data-source')
                if len(news_from)>0:
                    self.news_from = news_from[0].encode('utf-8')
                else:
                    news_from2 = tree.xpath('//div[@class="source"]/img/@alt')
                    if len(news_from2)>0:
                        self.news_from = news_from2[0].encode('utf-8')
                    else:
                        self.news_from = ''
                news_text = tree.xpath('//div[@id="ContentBody"]//p//text()')
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
                             with open('./eastmoney/%s/%s.jpg' %(part['name'],num) , 'wb') as f:
                                f.write(html)
                                paths = os.path.abspath('./eastmoney/%s/%s.jpg' %(part['name'],num))
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

if __name__=="__main__":
    em = easymoney_all_biz()
    em.getMain()
    print (u"东方财经其他 爬取完毕")