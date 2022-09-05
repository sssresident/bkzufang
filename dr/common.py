import hashlib    #1，首先引入hashlib模块
import os
import sqlite3
import pandas as pd
from mysql.mysqlldb import *
from drcms.settings import BASE_DIR
#加密
def pw_encrypt(pwd):
    md5 = hashlib.md5()  # 2，实例化md5() 方法

    md5.update(pwd.encode())  # 3，对字符串的字节类型加密

    result = md5.hexdigest()  # 4，加密

    return result

#上传数据文件
def upload_ajax(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')

        filepath=os.path.join(BASE_DIR, 'static', 'data')


        if not os.path.exists(filepath):
            try:
                os.makedirs(filepath)
            except:
                pass

        filepath=os.path.join(filepath,file_obj.name)

        f = open(filepath, 'wb')

        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()


        return str(filepath)

#写入数据库
def writedb(datapath,tablename,sheetname=""):
    '''

    :param datapath: 上传的文件路径
    :param tablename: 数据表名
    :return:
    '''

    if sheetname=="":
        df = pd.read_excel(datapath)
    else:
        df=pd.read_excel(datapath,sheet_name=sheetname)
    # df=df.dropna()
    dbpath = os.path.join(BASE_DIR, 'db.sqlite3')
    con = sqlite3.connect(dbpath)  # 如果路径里面没有这个数据库，会自动创建

    df.to_sql(tablename, con=con, if_exists='append', index=False)

