# coding:utf-8 #

import requests
import urllib2
from BeautifulSoup import BeautifulSoup


class WatchMan(object):
    @staticmethod
    def is_change():
        # r = requests.get('http://search.cnipr.com/search!dataScope.action')
        try:
            r = urllib2.urlopen('http://search.cnipr.com/search!dataScope.action')
            page = r
            print page
            # page = unicode(page).encode('utf-8')
            soup = BeautifulSoup((page))
            # text = ("中国发明专利").decode('utf-8')
            # target = soup.findAll('td',text=u"中国发明专利")
            target = soup.findAll('td')
            #数据库名称 数据范围 数据量
            if len(target) > 1:
                print target[1].contents
                return target[1].contents
        except Exception, e:
            print e
            pass
        return None  # WatchMan.is_change()

