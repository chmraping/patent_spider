# coding:utf8 #
__author__ = 'damon_lin'

from django.contrib.auth import *
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect

import json
def login_view(request):
    return render_to_response('login.html')


def auth(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    #u = User.objects.create_user(username, username, password)
    #u.save()
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        return HttpResponseRedirect('/index')
    else:
        return HttpResponseRedirect('/accounts/login')

def redirect_to_index(request):
    return HttpResponseRedirect('/index')

#退出登陆
@login_required
def unAuth(request):
    logout(request)
    return HttpResponse(json.dumps({"STATE":"SUCCESS"}))
