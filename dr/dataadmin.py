# -*- coding:utf-8 -*-

import math
import shutil

import numpy as np
from django.shortcuts import render
from django.shortcuts import HttpResponse

from mysql.mysqlldb import *
import json
import os,time,datetime
import pandas as pd
from dr.common import *

'''''---------------
----页面控制器
------------------'''
#获取字段
def getfield(tablename):
    field=sel_field(tablename)
    return field
def gethearder(tablename,arr1,arr2):
    field = getfield(tablename)
    header = []
    for i in field:
        if i not in arr1:
            if i in arr2:
                header.append({'key': i, 'width': 'auto', 'sort': True})
            else:
                header.append({'key': i, 'width': 'auto'})
    return header
def gettimes(tablename):
    times = sel_data("*", "timestamps", f"tablename='{tablename}'")
    timeStamp = times[0]['timestamp']
    timeArray = time.localtime(timeStamp)
    times = time.strftime("%m/%d/%Y", timeArray)
    return times
def getfilterarr(tablename,field):
    arr = ["---ALL---"]
    rs = sel_sql(f"SELECT {field} FROM {tablename} GROUP BY {field}")
    for i in rs:
        arr.append(i[field])
    return arr

def list_data(request):
    page = 1
    page = (page-1)*10
    tablename="data"
    rs=sel_data("*",tablename,"",f"LIMIT {page},10")
    arr1=["index"]
    arr2=["面积","月租"]
    header=gethearder(tablename,arr1,arr2)

    area=getfilterarr(tablename,'行政区')
    huxing = getfilterarr(tablename, '户型')



    rsall=sel_data("*",tablename)
    pages = math.ceil(len(rsall) / 10)

    return render(request, "admin\\list-data.html", {
         "tb": json.dumps(rs),"header":json.dumps(header),"area":json.dumps(area),"huxing":json.dumps(huxing),

       'pages':pages,'cur':1,'total':len(rsall)}
                  )
def list_datajson(request):
    postdata = request.POST
    page = int(postdata['page'])
    pagenum = (page-1)*10

    tablename="data"
    key1 = postdata['key1'].replace("---ALL---", "")
    key2 = postdata['key2'].replace("---ALL---", "")
    zhu1 = postdata['zhu1']
    if zhu1=="":
        zhu1=0
    zhu2 = postdata['zhu2']
    if zhu2=="":
        zhu2=9999999
    mian1 = postdata['mian1']
    if mian1 == "":
        mian1 = 0
    mian2 = postdata['mian2']
    if mian2=="":
        mian2=9999999

    wheres = f"行政区 like '%{key1}' and 户型 like '%{key2}' "
    wheres += f"and 月租 >={zhu1} and 月租<={zhu2} "
    wheres += f"and 面积 >={mian1} and 面积<={mian2} "
    rs=sel_data("*",tablename,wheres,f"LIMIT {pagenum},10")

    rsall=sel_data("*",tablename,wheres)
    pages = math.ceil(len(rsall) / 10)

    result = {'code':1,'pages': pages, 'cur': page, 'total': len(rsall), "tb": rs}

    return HttpResponse(json.dumps(result))

#各区房源数量统计
def area_chart(request):

    tablename="data"
    rs=sel_data("*",tablename)
    df=pd.DataFrame(rs)
    areagroup = dict(df.groupby('行政区').size())

    datas=[]
    for k,v in areagroup.items():
        datas.append({"value":int(v),"name":k})

    #print(datas)
    return render(request, "admin\\areachart.html", {
         "datas": json.dumps(datas)}
                  )

#按户型分类统计
def housetype_chart(request):

    tablename="data"
    rs=sel_data("*",tablename)
    df=pd.DataFrame(rs)
    housetype = dict(df.groupby('户型').size())
    #housetype = sorted(housetype.items(), key=lambda kv: (kv[1]), reverse=True)

    datas=[]
    for k,v in housetype.items():
        if int(v)>50:
            datas.append({"value":int(v),"name":k})

    #print(datas)
    return render(request, "admin\\housetypechart.html", {
         "datas": json.dumps(datas)}
                  )

#各区平均月租排行
def rent_chart(request):

    tablename="data"
    rs=sel_data("*",tablename)
    df=pd.DataFrame(rs)
    # 各区平均月租
    rent = dict(df.groupby('行政区').agg({'月租': np.average}))
    rent = dict(rent['月租'])
    for k, v in rent.items():
        rent[k] = int(v)
    rent = sorted(rent.items(), key=lambda kv: kv[1], reverse=True)

    labels=[]
    datas = []
    for item in rent:
        labels.append(item[0])
        datas.append(item[1])


    return render(request, "admin\\rentechart.html", {
         "datas": json.dumps(datas), "labels": json.dumps(labels)}
                  )



#各区房源面积统计
def mianji_chart(request):

    tablename="data"
    rs=sel_data("*",tablename)
    df=pd.DataFrame(rs)

    m0_50=df[(df.面积>0) & (df.面积 <=50)]
    m50_100 = df[(df.面积 > 50) & (df.面积 <= 100)]
    m100_150 = df[(df.面积 > 100) & (df.面积 <= 150)]
    m150 = df[(df.面积 > 150) & (df.面积 <= 9999999)]

    m0_50g=dict(m0_50.groupby('行政区').size())
    m50_100g = dict(m50_100.groupby('行政区').size())
    m100_150g = dict(m100_150.groupby('行政区').size())
    m150g = dict(m150.groupby('行政区').size())
    def ranarr(area):
        return [int(m0_50g[area]),int(m50_100g[area]),int(m100_150g[area]),int(m150g[area])]

    louhu=ranarr('罗湖区')
    guangmin = ranarr('光明区')
    nansa = ranarr('南山区')
    pinsa = ranarr('坪山区')
    dapeng = ranarr('大鹏新区')
    baoan = ranarr('宝安区')
    yantian = ranarr('盐田区')
    futian = ranarr('福田区')
    longhua = ranarr('龙华区')
    longgang = ranarr('龙岗区')

    datas=[louhu,guangmin,nansa,pinsa,dapeng,baoan,yantian,futian,longhua,longgang]

    return render(request, "admin\\mianjichart.html", {
         "datas": json.dumps(datas)}
                  )

#导入
def importdata(request):
    datapath = upload_ajax(request)  # 上传的文件
    # 写入数据库
    writedb(datapath, "data")

    data = {
        'code': 1
    }
    return HttpResponse(json.dumps(data))