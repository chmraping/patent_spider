# coding:utf-8
from django.db import models

# Create your models here.

class expression(models.Model):
	class Meta:
		db_table = 'expressionmanager_expression'

	# 公式名字
	name = models.CharField(max_length=3000, blank=True)
	# 表达式内容
	content = models.TextField()
	#表达式所属类别，是行业还是公司
	type = models.CharField(max_length=3000)


class excute_record(models.Model):
	class Meta:
		db_table = 'expressionmanager_excute_record'

	# 本次执行记录对应的表达式
	expression = models.ForeignKey(expression)
	# 执行的时间
	time_stamp = models.CharField(max_length=3000)


class patent(models.Model):
	class Meta:
		db_table = 'expressionmanager_patent'

	# 对应的执行记录
	record = models.ForeignKey(excute_record)

	# 申请号
	apply_number = models.CharField(max_length=100)

	#名称
	name = models.TextField()

	#主分类号
	main_classify_code = models.TextField()

	#分类号
	classify_code = models.TextField()

	#申请（专利权）人
	apply_man = models.TextField()

	#发明（设计）人
	invente_man = models.TextField()

	#公开（公告）日
	publicity_date = models.CharField(max_length=3000)

	#公开（公告）号
	publicity_code = models.CharField(max_length=3000)

	# 专利代理机构
	patent_agent = models.TextField()

	# 代理人
	agent = models.TextField()
	# 申请日
	aplly_date = models.CharField(max_length=3000)

	# 地址
	address = models.TextField()

	# 优先权
	priority = models.TextField()

	# 国省代码
	province_code = models.TextField()

	# 摘要
	abstract = models.TextField()

	# 主权项
	main_right = models.TextField()

	# 国际申请
	international_apply = models.TextField()

	# 国际公布
	international_publicity = models.TextField()

	# 进入国家日期
	enter_country_date = models.CharField(max_length=3000)

	# 权利要求书
	right_demand = models.TextField()

	# 法律状态
	valid_state = models.CharField(max_length=3000)

	# 专利状态代码
	state_code = models.CharField(max_length=3000)

	#录入时间
	spider_time = models.DateTimeField(null=True, auto_now_add=True)
	# 专利类型
	type = models.CharField(max_length=500, default="")


class setting(models.Model):
	class Meta:
		db_table = 'expressionmanager_setting'

	# 专利数量
	patent_num = models.CharField(max_length=3000)

	# 定时间隔
	scrap_delay = models.IntegerField(default=1)

	#标志位 是否在抓取
	is_scraping = models.BooleanField(default=False)

	#标志位 是否在监控
	loop = models.BooleanField(default=False)


class logdata(models.Model):
	class Meta:
		db_table = 'expressionmanager_logdata'

	# 抓取纪录
	content = models.TextField()
	# 抓取到第几条
	count = models.CharField(max_length=100, default=1)


class history_log(models.Model):
	class Meta:
		db_table = 'expressionmanager_history_log'

	# 开始时间
	start_time = models.DateTimeField(null=True, auto_now_add=True)
	# 结束时间
	end_time = models.DateTimeField(null=True, auto_now=True)
	#执行时间
	work_time = models.CharField(max_length=100)
	#开始日期
	start_day = models.CharField(max_length=100)
	#截止日期
	end_day = models.CharField(max_length=100)
	#表达式起始ID
	start_id = models.CharField(max_length=100, default=1)
	#表达式截止ID
	end_id = models.CharField(max_length=100)
	#状态（成功或者失败）
	state = models.CharField(max_length=100, default='失败')