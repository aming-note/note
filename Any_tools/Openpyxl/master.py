#coding:utf8
from openpyxl import *
wb = load_workbook(filename=r'服务器整理11-11.xlsx')     #传递Excel文件给ex变量
first_sheet = wb[wb.sheetnames[0]]
print(first_sheet["A2"].value)