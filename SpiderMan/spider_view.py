# coding=utf8

from  spider import spider
from ExpressionManager.models import *
from  ExpressionManager.models import setting
from django.http import HttpResponse
from ExpressionManager.ultis.excel_utils import excel_table_byindex
import time
import os.path
from watchman import WatchMan
import thread
import time
from django.contrib.auth.decorators import login_required
import json
import os
from ExpressionManager.ultis.log_utils import logger
# 在实际部署中，采用同一个进程中的标志位会遇到问题。因为nginx和uwsgi都是多进程的。
#   有空试试单例模式
#线程启动停止标志位
#loop = False
#是否正在抓取标志位
#is_scraping = False

def get_loop():
	set = setting.objects.get(id=1)
	return set.loop


def set_loop(val):
	set = setting.objects.get(id=1)
	set.loop = val
	set.save()


def get_scraping():
	set = setting.objects.get(id=1)
	return set.is_scraping


def set_scraping(val):
	set = setting.objects.get(id=1)
	set.is_scraping = val
	set.save()


def work_thread(temp):
	set = setting.objects.get(id=1)
	last_num = set.patent_num
	delay = set.scrap_delay
	logger.log('last_num: ' + last_num)
	while (get_loop()):
		num = WatchMan.is_change()
		if num == None:
			continue
		logger.log('get the num: ' + str(num[0]))
		if str(num) != last_num:
			set.patent_num = num
			set.save()
			set = setting.objects.get(id=1)
			last_num = set.patent_num
			logger.log('last_num: ' + last_num)
			logger.log("catch it !")
			#
			set_scraping(True)
			scrap()
			set_scraping(False)
			#
			set_loop(False)
		logger.log("wathman is running !" + time.strftime("%y-%m-%d %H:%M"))

		#seconds
		time.sleep(delay)


def reset(request):
	set = setting.objects.get(id=1)
	set.is_scraping = 0
	set.loop = 0
	set.save()
	return HttpResponse('重置成功！')


@login_required
def watch(request):
	if get_scraping() == True:
		return HttpResponse('正在抓取，无法开启监控！')
	if get_loop() == True:
		return HttpResponse('已经开启监控，请勿重复开启！')
	set_loop(True)
	thread.start_new_thread(work_thread, (1,))
	logger.log('continue')
	#等待一段时间，让线程跑起来
	time.sleep(20)
	return HttpResponse('ok')


@login_required
def stop(request):
	if get_scraping():
		return HttpResponse('正在抓取中，无法关闭监控！')
	set_loop(False)
	return HttpResponse('ok')


@login_required
def spider_view(request):
	if get_scraping() == True:
		return HttpResponse('正在抓取,请勿重复操作！')
	# if loop == True:
	#     return HttpResponse('已经开启监控，！')
	p = request.POST
	start_day = p['start_day']
	end_day = p['end_day']
	start_id = p['start_id']
	end_id = p['end_id']

	set_scraping(True)
	scrap(start_day, end_day, start_id, end_id)
	set_scraping(False)
	return HttpResponse('抓取完毕')


def scrap(start_day=None, end_day=None, start=1, end=20):
	logger.clear()
	logger.begin(start_day, end_day, start)
	logger.log("Try to get expressions...", flush=True)
	if end != None:
		expressions = expression.objects.filter(id__range=(start, end)).order_by('id')
	else:
		expressions = expression.objects.filter(id__range=(start, 3000)).order_by('id')

	s = spider()
	logger.log("Try to login...", flush=True)
	browser = s.login()
	cnt = 0
	file_path = ''
	for item in expressions:
		cnt += 1
		logger.log(u"第" + str(item.id) + u"个表达式:" + item.name, count=item.id, flush=True)
		#验证是否登录
		check_login = s.check_login(browser)
		if not json.loads(check_login)['success']:
			logger.log('check is not login , sleep 100s ,then try login again')
			time.sleep(100)
			browser = s.login()

		file_path = s.get_xls_by_expression(item.content, browser, start_day, end_day)
		if file_path != None:
			file_path = os.path.normpath(file_path)
			#logger.log(file_path)
			rows = excel_table_byindex(file_path, include_name=False)
			#删除文件
			os.remove(file_path)
			for row in rows:
				# 忽略第一行
				if row == rows[0]:
					continue
				apply_num = row[0]
				# 查重
				p = patent.objects.filter(apply_number=apply_num)
				if len(p) > 0:
					logger.log("{0} update!".format(apply_num))
					p = p[0]
					records = excute_record.objects.filter(expression=item, time_stamp=row[6])
					if len(records) > 0:
						record = records[0]
					else:
						record = excute_record(expression=item, time_stamp=row[6])
						record.save()
					p.record = record
					p.apply_number = row[0]
					p.name = row[1]
					p.main_classify_code = row[2]
					p.classify_code = row[3]
					p.apply_man = row[4]
					p.invente_man = row[5]
					p.publicity_date = row[6]
					p.publicity_code = row[7]
					p.patent_agent = row[8]
					p.agent = row[9]
					p.aplly_date = row[10]
					p.address = row[11]
					p.priority = row[12]
					p.province_code = row[13]
					p.abstract = row[14]
					p.main_right = row[15]
					p.international_apply = row[16]
					p.international_publicity = row[17]
					p.enter_country_date = row[18]
					p.right_demand = row[20]
					p.valid_state = row[21]
					p.state_code = row[22]
					p.type = row[23]
					p.save()
					continue
				logger.log(apply_num)
				#插入纪录
				records = excute_record.objects.filter(expression=item, time_stamp=row[6])  # row[6]==public data #
				if len(records) > 0:
					# logger.log("record already exist !")
					record = records[0]
				else:
					record = excute_record(expression=item, time_stamp=row[6])  # row[6]==public data #
					record.save()
				p = patent(  # 对应的执行记录
				             record=record,

				             # 申请号
				             apply_number=(row[0]),

				             # 名称
				             name=(row[1]),

				             # 主分类号
				             main_classify_code=row[2],

				             #分类号
				             classify_code=row[3],

				             #申请（专利权）人
				             apply_man=row[4],

				             #发明（设计）人
				             invente_man=row[5],

				             #公开（公告）日
				             publicity_date=(row[6]),

				             #公开（公告）号
				             publicity_code=row[7],

				             # 专利代理机构
				             patent_agent=row[8],

				             # 代理人
				             agent=row[9],
				             # 申请日
				             aplly_date=row[10],

				             # 地址
				             address=row[11],

				             # 优先权
				             priority=row[12],

				             # 国省代码
				             province_code=row[13],

				             # 摘要
				             abstract=row[14],

				             # 主权项
				             main_right=row[15],

				             # 国际申请
				             international_apply=row[16],

				             # 国际公布
				             international_publicity=row[17],

				             # 进入国家日期
				             enter_country_date=row[18],
				             # 权利要求书
				             right_demand=row[20],
				             # 法律状态
				             valid_state=row[21],
				             # 专利状态代码
				             state_code=row[22],
				             # 专利类型
				             type=row[23]
				             )
				try:
					p.save()
				except Exception, e:
					logger.log(str(e), flush=True)
					logger.log('failed to save patent!',flush=True)

	logger.log("--------Finish---------", flush=True)
	logger.finished()