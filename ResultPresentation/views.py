from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator
import json
from ExpressionManager.conf.conf import website
from ExpressionManager.models import excute_record, expression, patent
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def mainView(req):
	return render_to_response(website.mainView)


@login_required
def get_company(req, company):
	try:
		company_expression = expression.objects.get(name=company)
	except ObjectDoesNotExist:
		return HttpResponse(json.dumps({'STATE': "FAIL"}))

	record = company_expression.excute_record_set.all().order_by('time_stamp')
	times = [{"id": e.id, "time": e.time_stamp} for e in record]
	return HttpResponse(json.dumps(times))


@login_required
def get_record_detail(req, id):
	patents = patent.objects.filter(record__id=id)
	p = Paginator(patents, 10)
	if req.body == '':
		post = {}
	else:
		post = json.loads(req.body)
	if 'page' in post:
		page = post['page']
		ma = max(p.page_range)
		if 1 <= page <= ma:
			page = page
		else:
			page = 1
	else:
		page = 1

	patent_return = p.page(page)
	val = [{'name': e.name, 'stateCode': e.state_code, "abstract": e.abstract, "mainRight": e.main_right} for e
	       in patent_return]
	patent_count = p.count

	return HttpResponse(json.dumps({"patentCount": patent_count, "patents": val}))


def del_patent(request, company_name):
	global state
	try:
		company_expression = expression.objects.get(name=company_name)
		record = company_expression.excute_record_set.all()
		for e in record:
			patent.objects.filter(record=e.id).delete()
		state = 'SUCCESS'
	except Exception, e:
		print(e)
		state = 'FAILURE'

	return HttpResponse(state)