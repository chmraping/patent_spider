# coding:utf-8
from pyExcelerator import *
from ExpressionManager.models import *


global i, count
i = 0
count = 0
expressions = expression.objects.all()
w = Workbook()  # 创建一个工作簿
ws = w.add_sheet('sheet1')  # 创建一个工作表
for e in expressions:
	ws.write(i, 0, e.name)
	ws.write(i, 1, e.content)
	i += 1
	print(i)
try:
	w.save('expressions.xls')
except Exception, e:
	print e
	pass