"""drcms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from dr import admin, dataadmin



urlpatterns = [
    # 系统管理
    path('admin/', admin.index),
    path('', admin.index),

    path('admin/index', admin.index),
    path('admin/welcome', admin.welcome),
    path('admin/login', admin.login),

    path('admin/admin_list', admin.admin_list),
    path('admin/admin_deluser', admin.admin_deluser),
    path('admin/admin_adduser', admin.admin_adduser),
    path('admin/admin_add', admin.admin_add),
    path('admin/admin_reg', admin.admin_reg),
    path('admin/admin_edit', admin.admin_edit),
    path('admin/admin_edit2', admin.admin_edit2),
    path('admin/admin_edituser', admin.admin_edituser),



    #数据管理
    path('admin/list_data', dataadmin.list_data),#列表
    path('admin/list_datajson', dataadmin.list_datajson),
    path('admin/areachart', dataadmin.area_chart),
    path('admin/housetypechart', dataadmin.housetype_chart),
    path('admin/rentechart', dataadmin.rent_chart),
path('admin/mianjichart', dataadmin.mianji_chart),
path('admin/importdata', dataadmin.importdata),


]
