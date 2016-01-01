from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SpiderMan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload$','ExpressionManager.views.upload_view.get_upload'),
    url(r'upload_file$','ExpressionManager.views.upload_view.upload_file'),
    url(r'manager$','ExpressionManager.views.upload_view.manager_view'),
     url(r'get_expression/$','ExpressionManager.views.upload_view.get_expression'),
    url(r'add_expression$','ExpressionManager.views.upload_view.add_expression'),
    url(r'update_expression','ExpressionManager.views.upload_view.update_expression'),
    url(r'del_expression','ExpressionManager.views.upload_view.del_expression'),
    url(r'^index$','ResultPresentation.views.mainView'),
    url(r'^spider$','SpiderMan.spider_view.spider_view'),
    url(r'^watch$','SpiderMan.spider_view.watch'),
    url(r'^stop$','SpiderMan.spider_view.stop'),
    url(r'^accounts/login', 'SpiderMan.login.login_view'),
    url(r'^$', 'SpiderMan.login.redirect_to_index'),
    url(r'^auth$','SpiderMan.login.auth'),
    url(r'^unAuth$','SpiderMan.login.unAuth'),
    url(r'^get_company/(\w+)','ResultPresentation.views.get_company'),
    url(r'^del_patent/(\w+)','ResultPresentation.views.del_patent'),
    url(r'^get_record_detail/(\d+)','ResultPresentation.views.get_record_detail'),
    url(r'^set_setting$','SpiderMan.setting_view.set_setting'),
    url(r'^get_setting$','SpiderMan.setting_view.get_setting'),
    url(r'^fuzzy_query','SpiderMan.query_view.fuzzy_query'),
    url(r'^reset','SpiderMan.spider_view.reset'),
    url(r'^log','SpiderMan.log_view.get_log'),
    url(r'^history', 'SpiderMan.log_view.get_history_view'),
    url(r'^get_history_detail','SpiderMan.log_view.get_history_detail'),

)
