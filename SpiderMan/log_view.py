# coding:utf-8 #
__author__ = 'damon_lin'

from ExpressionManager.models import logdata, history_log
from ExpressionManager.conf.conf import website
from django.shortcuts import render_to_response
from django.http import *
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage


def date_handler(obj):
	return obj.strftime('%Y—%m-%d,%H:%M:%S')


def get_log(request):
	# log = logdata.objects.get(id=1)
	log = logdata.objects.last()
	return HttpResponse(log.content)


def get_history_view(request):
	return render_to_response(website.history)


def get_history_detail(request):
	history = history_log.objects.all().order_by("-id")
	pages = Paginator(history, 10)
	# json.load(request.body)
	if request.body == '':
		post = {}
	else:
		post = json.loads(request.body)
	if 'page' in post:
		page = post['page']
	else:
		page = 1
	try:
		histories_return = pages.page(page)
	except EmptyPage:
		histories_return = pages.page(pages.num_pages)
	val = [{'start_time': e.start_time, 'end_time': e.end_time, 'start_id': e.start_id, 'end_id': e.end_id,
	        'work_time': e.work_time, 'start_day': e.start_day, 'end_day': e.end_day, 'state': e.state} for e in
	       histories_return]
	return HttpResponse(json.dumps({'histories': val, 'historiesCount': pages.count}, default=date_handler))
