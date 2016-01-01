# coding:utf-8
__author__ = 'damon-lin'

from django.conf import settings
settings.configure()
from ExpressionManager.ultis.excel_utils import excel_table_byindex
from  ExpressionManager.models import patent
from  ExpressionManager.models import excute_record

dic = {
    # 对应的执行记录
    u'对应的执行记录': 1,

    # 申请号
    u'申请号': 2,

    #名称
    u'名称': 3,

    #主分类号
    u'主分类号': 4,

    #分类号
    u'分类号': 5,

    #申请（专利权）人
    u'申请（专利权）人': 6,

    #发明（设计）人
    u'发明（设计）人': 7,

    #公开（公告）日
    u'公开（公告）日': 8,

    #公开（公告）号
    u'公开（公告）号': 9,

    # 专利代理机构
    u'专利代理机构': 10,

    # 代理人
    u'代理人': 11,
    # 申请日
    u'申请日': 12,

    # 地址
    u'地址': 13,

    # 优先权
    u'优先权': 14,

    # 国省代码
    u'国省代码': 15,

    # 摘要
    u'摘要': 16,

    # 主权项
    u'主权项': 17,

    # 国际申请
    u'国际申请': 18,

    # 国际公布
    u'国际公布': 19,

    # 进入国家日期
    u'进入国家日期': 20,

    # 权利要求书
    u'权利要求书':22,

    u'法律状态':23,

    u'专利状态代码':24
}


def import_from_xls(file):
    rows = excel_table_byindex(file)
    for row in rows:
        patent_data = []
        cnt =100
        while (cnt>0):
            cnt-=1
            patent_data.append(0)
        for key in row:
            print key, row[key]
            if len(row[key])>0:
                patent_data[dic[key]] = row[key]
        #record = excute_record()
        temp_patent = patent(  # 对应的执行记录
                               #record=patent_data[1],
                               # 申请号
                               apply_number=patent_data[2],
                               #名称
                               name=patent_data[3],
                               #主分类号
                               main_classify_code=patent_data[4],
                               #分类号
                               classify_code=patent_data[5],
                               #申请（专利权）人
                               apply_man=patent_data[6],
                               #发明（设计）人
                               invente_man=patent_data[7],
                               #公开（公告）日
                               publicity_date=patent_data[8],
                               #公开（公告）号
                               publicity_code=patent_data[9],
                               # 专利代理机构
                               patent_agent=patent_data[10],
                               # 代理人
                               agent=patent_data[11],
                               # 申请日
                               aplly_date=patent_data[12],
                               # 地址
                               address=patent_data[13],
                               # 优先权
                               priority=patent_data[14],
                               # 国省代码
                               province_code=patent_data[15],
                               # 摘要
                               abstract=patent_data[16],
                               # 主权项
                               main_right=patent_data[17],
                               # 国际申请
                               international_apply=patent_data[18],
                               # 国际公布
                               international_publicity=patent_data[19],
                               # 进入国家日期
                               enter_country_date=patent_data[20],
                               right_demand = patent_data[22],
                               valid_state=patent_data[23],
                               state_code=patent_data[24])
        temp_patent.save()
