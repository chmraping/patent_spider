# coding:utf-8 #
__author__ = 'damon_lin'
from ExpressionManager.lib import *
from django.contrib.auth.decorators import login_required

@login_required
def fuzzy_query(request):
    query = request.GET['query']
    exp = expression.objects.filter(name__contains=query)[0:100]
    name=[]
    for item in exp:
        name.append(item.name)
        print item.name
    return HttpResponse(json.dumps({"query":query,"name":name}))
