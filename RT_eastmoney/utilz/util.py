# coding=utf-8
import re, requests, uuid
import cPickle
requests.packages.urllib3.disable_warnings()
'''
通用的get方法
url：请求的url地址
headers：请求的头信息数据，是以字典形式存在的
cookies：请求的cookies信息数据，以字典形式存在
proxies：代理IP地址，字典
params：get方式中？号后面的一大串数据，url地址截至到？以前
timeout：客户端与服务器的连接时常

参数默认值设置
'''
def get(url, cookie=None, proxies=None, param=None, header=None):
    s = requests.session()
    ret = {}
    ret["issuccess"] = False
    try:
        if cookie is not None:
            s.cookies = cookie
        if proxies is not None:
            s.proxies = proxies
        if param is not None:
            s.params = param
        if header is not None:
            s.headers = header
        r = s.get(url=url, verify=False, timeout=20)
        html = r.content
        if html:
            ret["issuccess"] = True
            ret["message"] = html
            ret["cookie"] = s.cookies
    except Exception, ex:
        print (ex.message)
    finally:
        if s:
            s.close()
    return ret

'''
通用post方式

url：请求的url地址
headers：请求的头信息数据，是以字典形式存在的
cookies：请求的cookies信息数据，以字典形式存在
proxies：代理IP地址，字典
params：get方式中？号后面的一大串数据，url地址截至到？以前
timeout：客户端与服务器的连接时常
data：同form表单，对应与form中的id，键，也是字典形式的

参数默认值设置
cookies的设置不能放在headers当中，不能将它以字符串的形式进行请求访问
如果想带cookies直接访问   个人主页  等信息，只能将cookies转变成字典格式
即：
s.cookies["Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac"]="1506045816"
s.cookies["__message_cnel_msg_id"]="0"
s.cookies["BT"]="1505968296151"
'''
def posts(url, data, params=None, proxies=None, timeout=20, cookies=None, headers=None, verify=None):
    # 建立与服务端的会话
    s = requests.session()
    ret = {}
    # 返回值数据
    ret["issucess"] = 0
    ret["message"] = ""
    try:
        # 如果params有信息，则设置params
        if params is not None:
            s.params = params
        # 如果proxies有效，则设置proxies
        if proxies is not None:
            s.proxies = proxies
        # 默认设置timeout为20秒，可自定义设置
        if timeout != 20:
            s.timeout = timeout
        # 如果cookies有效，则设置cookies
        if cookies is not None:
            s.cookies = cookies
        # 如果headers有效，则设置headers
        if headers is not None:
            s.headers = headers
        # 发送请求包
        r = s.post(url, data=data, verify=False)
        if r:
            ret["issucess"] = 1
            ret["message"] = r.content
            ret["cookie"] = cPickle.dumps(s.cookies)
    except Exception, ex:
        # 异常处理
        print ex.message
        ret["message"] = ex.message
    finally:
        # 关闭本次会话
        if s:
            s.close()
    # 返回数据
    return ret
'''
涉及到并发的情况下，不要使用id自增的方式对数据库表设置自增字段，
uuid局域网内的计算机由操作系统产生的一串字符，不会重复
只要涉及到并发，我们可以采用UUID作为主键
数据表当中还要配合一个时间字段（insertTime）使用，这样无论是反应日志或是部门之间的对接，
都能有很有效的证据
'''
def getUUID():
    return str(uuid.uuid4())


'''
去除html标签的方法，如果我们不想要获取到的数据中有html标签，可调用此方法进行处理
'''
def getNoHtmlBody(content):
    body = None
    try:
        content = content.replace('</P>', '\n')
        dr = re.compile(r'<[^>]+>')
        body = dr.sub('', content)
    except Exception, ex:
        print (ex.message)
    return body
