# coding:utf-8
__author__ = 'damon-lin'
import json

from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from ExpressionManager.lib import *
from ExpressionManager.ultis.excel_utils import *


class UploadFileForm(forms.Form):
	file = forms.FileField()


# 获得上传视图
@login_required
def get_upload(requset):
	# print(requset.META)
	return render_to_response(website.upload)


# 返回管理视图
@login_required
def manager_view(request):
	return render_to_response(website.manager)


# 新增表达式
@login_required
def add_expression(request):
	name = request.POST['name']
	content = request.POST['content']
	temp_expression = expression(name=name, content=content)
	temp_expression.save()
	return HttpResponse(json.dumps({'state': 'SUCCESS', 'id': temp_expression.id}))


# 删除表达式
@login_required
def del_expression(request):
	expression_id = request.POST['id']
	try:
		temp_expression = expression.objects.get(id=expression_id)
		temp_expression.delete()
	except Exception, e:
		print(e)
		return HttpResponse("erro")
	return HttpResponse('SUCCESS')


# 更改表达式
@login_required
def update_expression(request):
	id = request.POST['id']
	name = request.POST['name']
	content = request.POST['content']
	temp_expression = expression.objects.get(id=id)
	temp_expression.name = name
	temp_expression.content = content
	temp_expression.save()
	return HttpResponse(json.dumps({'state': 'SUCCESS'}))


#返回表达式数据
@login_required
def get_expression(request):

	cur_page = request.GET.get('cur_page')
	records_per_page = request.GET.get('records_per_page')
	filter_by = request.GET.get('filterBy')
	filter_value = request.GET.get('filterValue')
	if filter_by is None or filter_value is None:
		expressions = expression.objects.all().order_by('id')
	else:
		if filter_by == 'id':
			expressions = expression.objects.filter(id__contains=filter_value)
		else:
			expressions = expression.objects.filter(name__contains=filter_value)

	pages = Paginator(expressions, records_per_page)
	if cur_page is None:
		cur_page = 1
	try:
		data = pages.page(cur_page)
	except EmptyPage:
		data = pages.page(pages.num_pages)
	json_data = []
	for item in data:
		json_data.append({'name': item.name, 'content': item.content, 'id': item.id})
	#return HttpResponse(json.dumps(json_data, ensure_ascii=False))
	return HttpResponse(json.dumps({'cur_page': int(cur_page)+1, 'totalRecords': pages.count, 'data': json_data}))


#获得上传的表达式文件，并写入数据库
@login_required
def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			tempFile = get_abs_dir("/TempFiles/temp.xls")
			file = request.FILES['file']
			destination = open(tempFile, 'wb+')
			write_file(destination, file)
			rows = excel_table_byindex(tempFile, include_name=False)
			for row in rows:
				temp_expression = expression(name=row[0], content=row[1])
				temp_expression.save()
			return HttpResponse('upload succeed !')
		return HttpResponse('form error !')
	else:
		return HttpResponse('methos erro !')


#获得文件的绝对路径
@login_required
def get_abs_dir(dir):
	base_dir = os.path.dirname(__file__)
	index = base_dir.index('/ExpressionManager')
	base_dir = base_dir[:index]
	tempFile = base_dir + dir
	return tempFile


#写入文件
@login_required
def write_file(destination, file):
	for chunck in file.chunks():
		destination.write(chunck)
	destination.close()