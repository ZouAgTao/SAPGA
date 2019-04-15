#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 2019.04.12
# author Agtao
#

import xlrd
import xlwt
import json

# 定义常量
file1 = "./1.xlsx"
file2 = "./2.xlsx"

def open_excel(filename):
    try:
        excel = xlrd.open_workbook(filename)
        return excel
    except:
        print("Excel文件打开错误")
        return None

def open_sheet(excel,sheet_name):
    try:
        sheet = excel.sheet_by_name(sheet_name)
        return sheet
    except:
        print("Sheet工作簿打开错误")
        return None

def get_list_a1():
    a1 = []

    excel = open_excel(file1)
    sheet = open_sheet(excel,"A侧进货口送至B侧指定出货口")

    for i in range(1,101):
        a1.append(int(sheet.cell(i,1).value))

    return a1

def get_list_a2():
    a2 = []

    excel = open_excel(file1)
    sheet = open_sheet(excel,"A侧进货口送至B侧指定出货口")

    for i in range(1,101):
        a2.append(int(sheet.cell(i,2).value))

    return a2

def write_array(lst,filename,sheetname,value):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet(sheetname)
    for i_lst in range(len(lst)):
        worksheet.write(i_lst+1, 0, str(lst[i_lst][0]))
        worksheet.write(i_lst+1, 1, str(lst[i_lst][1]))

    worksheet.write(1,3,str(value))

    workbook.save(filename)

# with open('data.json', 'r') as f:
#     result = json.load(f)
#     data = result[len(result)-1][1]
#
#     write_array(data,"data.xls","无长度-3辆车")