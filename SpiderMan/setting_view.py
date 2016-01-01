# coding:utf-8 #
__author__ = 'damon_lin'

from ExpressionManager.models import setting
from django.shortcuts import render_to_response
from django.http import *
import json
from django.contrib.auth.decorators import login_required

@login_required
def get_setting(request):
    set = setting.objects.get(id =1)
    wrap={'delay':set.scrap_delay}
    return HttpResponse(json.dumps(wrap))

@login_required
def set_setting(request):
    delay = request.POST['delay']
    set = setting.objects.get(id=1)
    set.scrap_delay = delay
    set.save()
    return HttpResponse(json.dumps({'status':'success'}))
