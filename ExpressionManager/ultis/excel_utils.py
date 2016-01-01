# coding:utf-8
__author__ = 'damon-lin'
import xdrlib, sys
import xlrd

def open_excel(file='./file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception, e:
        print str(e)


# 根据索引获取Excel表格中的数据
# 参数:file：Excel文件路径
# colnameindex：表头列名所在行的索引
# by_index：表的索引
def excel_table_byindex(file='./file.xls', colnameindex=0, by_index=0,include_name = True):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  #行数
    ncols = table.ncols  #列数
    colnames = table.row_values(colnameindex)  #某一行数据
    list = []
    if include_name:
        start_index = 1
    else:
        start_index = 0
    for rownum in range(start_index, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                if include_name:
                    app[colnames[i]] = row[i]
                else:
                    app[i] = row[i]
            list.append(app)
    return list


#根据名称获取Excel表格中的数据
# 参数:file：Excel文件路径
# colnameindex：表头列名所在行的所以
# by_name：Sheet1名称
def excel_table_byname(file, colnameindex=0, by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows  #行数
    colnames = table.row_values(colnameindex)  #某一行数据
    list = []

    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


def main():
    #根据索引获取内容
    tables = excel_table_byindex()
    for row in tables:
        print row[u'名称']

#  tables = excel_table_byname()
# for row in tables:
#     print row

if __name__ == "__main__":
    main()