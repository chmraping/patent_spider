# coding=utf8
import urllib2
import urllib
import cookielib
import random
import json
import os
import time
import uuid
from ExpressionManager.dao.expression_import_xls import import_from_xls

def login(user='sfj096', pwd='254981'):
    login_url = "http://search.cnipr.com/login!goonlogin.action?rd=" + str(random.random())  #强制登陆
    check_login = "http://search.cnipr.com/login!checkLogin.action?randomNum=" + str(random.random())
    try:
        cj = cookielib.CookieJar()
        browser = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        browser.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        post_data = urllib.urlencode({'username': user, 'password': pwd})
        browser.open(login_url, post_data)
        login_success = browser.open(check_login)
        data = login_success.read()
        assert isinstance(data, object)
        json_data = json.loads(data)
        assert json_data['success'] == True, '登陆失败'
        print(json_data)
        return browser
    except Exception, e:
        print(str(e))


def get_data_by_expr(expr, dt=20150401):
    opener = login()
    begin = 1
    end = 2000
    download_url = "http://search.cnipr.com/downloadvip!download2000.action?rd" + str(random.random())
    downlist_url = "http://search.cnipr.com/downloadvip!downloadUserFile.action?rd=" + str(random.random())
    post_data = {'begin': begin, 'end': end,
                 'strWhere': expr + " and (" + str(dt) + ")/PD",
                 'filename': "著录项批量下载2014401",
                 'fields': "申请号;名称;主分类号;分类号;申请（专利权）人;发明（设计）人;公开（公告）日;公开（公告）号;专利代理机构;代理人;申请日;地址;优先权;国省代码;摘要;主权项;国际申请;国际公布;进入国家日期;分案原申请号;",
                 'source': 'FMZL,SYXX', 'strSortMethod': "-公开（公告）日", "option": "2",
                 }
    post_data = urllib.urlencode(post_data)
    file_url= None
    data = opener.open(download_url, post_data).read()
    json_data = json.loads(data)
    assert json_data['success']==True, "获取下载项失败"
    while(file_url==None):
         data_list = json.loads(opener.open(downlist_url).read())['downloadUserFiles']
         file_url = data_list[1]['fileurl']
    #print(data_list['downloadUserFiles'])
    print file_url
    return file_url


def downloadxls(url, filename):
    urllib.urlretrieve(url, os.path.join(os.getcwd(), str(filename) + ".xls"))
    return os.path.join(os.getcwd()+"\\"+str(filename) + ".xls")

#根据表达式下载文件，同时返回绝对路径的文件名
def get_xls_by_expression(expr):
    date = time.strftime("%Y%m%d", time.localtime(time.time()))
    download_url = get_data_by_expr(expr)
    filename = uuid.uuid1().int
    return downloadxls(download_url, filename)

#get_data_by_expr("""('深圳华为移动通信技术有限公司','华为机器有限公司','上海华为技术有限公司','华为数字技术有限公司','杭州华为三康技术有限公司','深圳市华为技术软件有限公司','深圳市华为电气股份有限公司','张家港市华为电子有限公司','成都鼎桥通信技术有限公司','北京华为数字技术有限公司','华为终端有限公司','深圳市华为电气技术有限公司','华为技术有限公司','深圳市华为技术有限公司','华为数字技术（成都）有限公司','聚信科技有限公司','深圳华为通信技术有限公司','华为技术服务有限公司')/PA""",
#                20150401)

file = get_xls_by_expression((
    """('深圳华为移动通信技术有限公司','华为机器有限公司','上海华为技术有限公司','华为数字技术有限公司','杭州华为三康技术有限公司','深圳市华为技术软件有限公司','深圳市华为电气股份有限公司','张家港市华为电子有限公司','成都鼎桥通信技术有限公司','北京华为数字技术有限公司','华为终端有限公司','深圳市华为电气技术有限公司','华为技术有限公司','深圳市华为技术有限公司','华为数字技术（成都）有限公司','聚信科技有限公司','深圳华为通信技术有限公司','华为技术服务有限公司')/PA"""))

#import_from_xls(file)

