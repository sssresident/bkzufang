# from django.contrib import admin

# Register your models here.
import datetime
import zipfile


from django.shortcuts import render,redirect
from django.http.request import HttpRequest
from django.shortcuts import HttpResponse
from dr.common import *
from mysql.mysqlldb import *
from captcha.fields import CaptchaField     # 一定要导入这行
import json

from drcms.settings import BASE_DIR

def index(request):
    # return render_to_response('index.html', {'title': 'This is Title', 'message': 'This is message'})
    if request.session.get('userinfo'):
        #userinfo = request.session.get('userinfo')
        return render(request,"admin\index.html",
                      {"title":"贝壳数据可视化租房助手"
                       })
    else:

        return redirect("/admin/login")

def clearnum(strs):
    a=["0","1","2","3","4","5","6","7","8","9"]
    for i in a:
        strs=strs.replace(i,"")
    return strs



def welcome(request=HttpRequest()):

    count1=sel_sql("SELECT COUNT(0) as num FROM data")

    count3 = sel_sql("SELECT COUNT(0) as num FROM user")


    rs=[
        {'name': '房源', 'num': count1[0]['num']},

        {'name': '用户', 'num': count3[0]['num']}
        ]



    return render(request,"admin\welcome.html",
                  {"datas":rs
                   })

#用户登录
def login(request):

    if request.method == "GET":



        return render(request,"admin\login.html",{"status":1})
    else:
        obj = request.POST  # request.POST拿到的是POST的数据



        rs= sel_data('*','user',"username='{0}' and password='{1}' and status=1".format(obj['username'],pw_encrypt(obj['password'])))

        if rs:
            request.session.set_expiry(None)
            request.session['userinfo'] = rs[0]

            return redirect("/admin/index")
        else:

            return render(request, "admin\login.html", {
                       "status":0,"uname":obj['username'],"title":"管理后台登录"
                       }
                          )


# 帐号列表

def admin_list(request):

    if request.GET:

        rs=sel_data("*","user","username like '%"+request.GET['username']+"%'")
    else:
        rs=sel_data("*","user")

    return render(request, "admin\\admin-list.html", {
        "datas": rs, "title": "管理后台登录"
    }
                  )

# 帐号编辑

def admin_edit(request):

    id= request.GET['id']
    rs = sel_data("*", "user","id="+id)
    return render(request, "admin\\admin-edit.html", {
        "datas": rs[0], "title": "管理后台"
    }
                  )

# 帐号编辑

def admin_edit2(request):

    id= request.GET['id']
    rs = sel_data("*", "user","id="+id)
    return render(request, "admin\\admin-edit2.html", {
        "datas": rs[0], "title": "管理后台"
    }
                  )

# 帐号增加

def admin_add(request):
    rs=sel_data("*","user")

    return render(request, "admin\\admin-add.html", {
        "datas": rs, "title": "管理后台登录"
    }
                  )

def admin_reg(request):
    rs=sel_data("*","user")

    return render(request, "admin\\admin-add2.html", {
        "datas": rs, "title": "管理后台登录"
    }
                  )

# 添加用户接口api
def admin_adduser(request):
    obj = request.POST  # request.POST拿到的是POST的数据
    arr = json.loads(obj['item'])
    adddatas={"username":arr["username"],"password":pw_encrypt(arr["pass"]),"name":arr["name"],"email":arr["email"],"role":arr["role"]}

    rs = ins_data("user",adddatas)
    if rs==1:
        data = {
            'status': 1,
            'msg': '用户新增成功！'
        }
    else:
        data = {
            'status': 1,
            'msg': '用户新增失败！'
        }

    return HttpResponse(json.dumps(data))

# 编辑用户接口api
def admin_edituser(request):
    obj = request.POST  # request.POST拿到的是POST的数据
    arr = json.loads(obj['item'])
    if len(arr["pass"])==32:
        adddatas={"username":arr["username"],"password":arr["pass"],"name":arr["name"],"email":arr["email"],"role":arr["role"]}
    else:
        adddatas={"username":arr["username"],"password":pw_encrypt(arr["pass"]),"name":arr["name"],"email":arr["email"],"role":arr["role"]}


    rs = save_data("user", adddatas,"id="+obj['id'])
    if rs == 1:
        data = {
            'status': 1,
            'msg': '保存成功！'
        }
    else:
        data = {
            'status': 1,
            'msg': '保存失败！'
        }
    return HttpResponse(json.dumps(data))

# 删除用户接口
def admin_deluser(request):
    obj = request.POST  # request.POST拿到的是POST的数据

    rs = del_data("user","id="+obj['id'])
    if rs == 1:
        data = {
            'status': 1,
            'msg': '删除成功！'
        }
    else:
        data = {
            'status': 1,
            'msg': '删除失败！'
        }
    return HttpResponse(json.dumps(data))
