# coding=utf8
import urllib2
import urllib
import cookielib
import random
import json
import os
import time
import uuid
import sys
from BeautifulSoup import BeautifulSoup
from ExpressionManager.ultis.log_utils import logger
import socket
socket.setdefaulttimeout(60)

class spider(object):
    def spider(self):
        pass

    # 带重发功能
    def re_transmission(self, url, opener, post_data=None,append=None):
        failed = True
        if post_data != None:
            u_post_data = {}
            for k, v in post_data.iteritems():
                u_post_data[k] = unicode(v).encode('utf-8')
            u_post_data = urllib.urlencode(u_post_data)
            if append != None:
                u_post_data+=('&channelId='+append)
            data = None
            while failed:
                try:
                    data = opener.open(url, u_post_data).read()
                    #logger.log("try to visit url:"+url+" success !", flush=True)
                    failed = False
                except Exception, e:
                    failed = True
                    logger.log("try to visit url:"+url+" failed !")
                    logger.log(str(e), flush=True)
                    pass
        else:
             while failed:
                try:
                    data = opener.open(url).read()
                    #logger.log("try to visit url:"+url+" success !", flush=True)
                    failed = False
                except Exception, e:
                    failed = True
                    logger.log("try to visit url:"+url+" failed !")
                    logger.log(str(e), flush=True)
                    pass
        return data

    #登陆
    def login(self, user='', pwd=''):
        try_login = "http://vip.cnipr.com/login.action?rd=" + str(random.random())  # 尝试登陆
        login_url = "http://vip.cnipr.com/login!goonlogin.action?rd=" + str(random.random())  # 强制登陆
        check_login = "http://vip.cnipr.com/login!checkLogin.action?randomNum=" + str(random.random())
        cnt=3
        while(cnt>0):
            cnt-=1
            try:
                cj = cookielib.CookieJar()
                browser = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                browser.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
                post_data = {'username': user, 'password': pwd}
                #######################
                data = self.re_transmission(try_login,browser,post_data)

                if json.loads(data)['msg'] == 'alreadylogin':
                    logger.log ("account already login !",flush=True)
                    cj = cookielib.CookieJar()
                    browser = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                    browser.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
                    post_data = {'username': user, 'password': pwd}
                    #######################
                    data = self.re_transmission(login_url,browser,post_data)

                    if json.loads(data)['msg'] != 'success':
                        logger.log('force login failed !',flush=True)
                        continue
                    logger.log('force login success !',flush=True)
                    return browser
                if data.find('success')==-1:
                    logger.log ("login failed !",flush=True)

                logger.log("login success !",flush=True)
                return browser

            except Exception, e:
                logger.log ("login catch exception !",flush=True)
                logger.log(str(e),flush=True)
                pass

     #根据表达式下载文件
    def get_data_by_expr(self, expr, opener, start_day=None, end_day=None):
        #check_login = self.check_login(opener)
        if opener != None:
            logger.log('login is not None !')
        else:
            logger.log('login is None !')
            return None
        begin = 1
        end = 2000
        search_url = "http://vip.cnipr.com/search!doOverviewSearch.action"
        if(start_day==end_day):
            date = time.strftime("%Y%m%d", time.localtime(time.time()))
            search_expr = expr + " and ("+str(start_day)+")/PD"
        else:
            search_expr = expr + " and (" + str(start_day) +" to "+str(end_day) +")/PD"
        #logger.log(search_expr)
        post_data = {
            'strWhere': search_expr,
            'start': 1,
            'saveFlag': 1,
            'limit': 10,
            'mpage': 'null',
            'channelId': 'SYXX',
            'mpage': 'advsch'
        }

        #######################
        data = self.re_transmission(search_url, opener, post_data,'FMZL')
        soup = BeautifulSoup(data)
        target = soup.findAll('div', {'class': 'g_item'})
        length = len(target)
        logger.log ("length of items:"+str(length), format(True))
        if length < 1:
            logger.log ("The search result is None,don't need to scrap !")
            return None
        # g_item
        # logger.log data
        #logger.log str(target)
        download_url = "http://vip.cnipr.com/downloadvip!download2000.action?rd" + str(random.random())
        downlist_url = "http://vip.cnipr.com/downloadvip!downloadUserFile.action?rd=" + str(random.random())
        post_data = {'begin': begin, 'end': end,
                     'strWhere': search_expr,
                     'filename': u"著录项批量下载2014401",
                     'fields': u"申请号;名称;主分类号;分类号;申请（专利权）人;发明（设计）人;公开（公告）日;公开（公告）号;专利代理机构;代理人;申请日;地址;优先权;国省代码;摘要;主权项;国际申请;国际公布;进入国家日期;分案原申请号;权利要求书;法律状态;专利权状态代码",
                     'source': 'FMZL,SYXX,WGZL', 'strSortMethod': u"-公开（公告）日", "option": "2",
                     }
        try:
            file_url = None
            #######################
            data = self.re_transmission(download_url, opener, post_data)

            json_data = json.loads(data)
            assert json_data['success'] == True, "获取下载项失败"
        except Exception, e:
            logger.log("Get the download file catch exception !",flush=True)
            logger.log(str(e),flush=True)


        cnt = 1
        # logger.log ("try to get download file !", flush=True)
        while (file_url == None and cnt < 100):
            #######################
            logger.log("try to get download file {0} times!".format(cnt), flush=True)
            data = self.re_transmission(downlist_url,opener)

            data_list = json.loads(data)['downloadUserFiles']
            file_url = None
            if data_list is not None:
                file_url = data_list[0]['fileurl']
                cnt += 1
        # logger.log(data_list['downloadUserFiles'])
        if file_url is not None:
            file_url = 'http://vip' + file_url[13:]
        else:
            logger.log('timeout to get download URL', flush=True)

        logger.log(file_url, flush=True)
        return file_url

    #更具url下载文件
    def downloadxls(self, url, filename):
        urllib.urlretrieve(url, os.path.join(os.getcwd(), str(filename) + ".xls"))
        return os.path.join(os.getcwd(), str(filename) + ".xls")


    # 根据表达式下载文件，同时返回绝对路径的文件名
    def get_xls_by_expression(self, expr, browser,start_day=None,end_day=None):
        date = time.strftime("%Y%m%d", time.localtime(time.time()))
        download_url = self.get_data_by_expr(expr, browser,start_day,end_day)
        if download_url == None:
            return None
        filename = uuid.uuid1().int
        return self.downloadxls(download_url, filename)

        # get_data_by_expr("""('深圳华为移动通信技术有限公司','华为机器有限公司','上海华为技术有限公司','华为数字技术有限公司','杭州华为三康技术有限公司','深圳市华为技术软件有限公司','深圳市华为电气股份有限公司','张家港市华为电子有限公司','成都鼎桥通信技术有限公司','北京华为数字技术有限公司','华为终端有限公司','深圳市华为电气技术有限公司','华为技术有限公司','深圳市华为技术有限公司','华为数字技术（成都）有限公司','聚信科技有限公司','深圳华为通信技术有限公司','华为技术服务有限公司')/PA""",
        # 20150401)

        # file = get_xls_by_expression((
        # """('深圳华为移动通信技术有限公司','华为机器有限公司','上海华为技术有限公司','华为数字技术有限公司','杭州华为三康技术有限公司','深圳市华为技术软件有限公司','深圳市华为电气股份有限公司','张家港市华为电子有限公司','成都鼎桥通信技术有限公司','北京华为数字技术有限公司','华为终端有限公司','深圳市华为电气技术有限公司','华为技术有限公司','深圳市华为技术有限公司','华为数字技术（成都）有限公司','聚信科技有限公司','深圳华为通信技术有限公司','华为技术服务有限公司')/PA"""))

        # import_from_xls(file)

    def check_login(self, browser):
        check_login = "http://vip.cnipr.com/login!checkLogin.action?randomNum=" + str(random.random())
        data = browser.open(check_login).read()
        return data




