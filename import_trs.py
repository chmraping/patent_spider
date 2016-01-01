#!/usr/bin/python
# coding=utf8
import MySQLdb
from ExpressionManager.models import *
from ExpressionManager.ultis.excel_utils import excel_table_byindex


def begin():
	file_path = './test.xls'
	rows = excel_table_byindex(file_path, include_name=False)

	for row in rows:
		# 忽略第一行
		if row == rows[0]:
			continue
		apply_num = row[0]
		# 查重
		p = patent.objects.filter(apply_number=apply_num)
		if len(p) > 0:
			print("{0} update!".format(apply_num))
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