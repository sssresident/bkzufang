from django.db import connections


def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [
    dict(zip([col[0] for col in desc], row))
    for row in cursor.fetchall()
    ]
def sel_data(filed,tablename,wheres="",other=""):
    cursor = connections['default'].cursor()
    if wheres=="":
        sqls='select {0} from {1} {2}'.format(filed,tablename,other)
    else:
        sqls='select {0} from {1} where {2} {3}'.format(filed,tablename,wheres,other)


    cursor.execute(sqls)
    # fetchall返回的是元祖...
    #rs = cursor.fetchall()
    rs=dictfetchall(cursor)
    cursor.close()
    return rs


def ins_data(tablename,dicts):

    cursor = connections['default'].cursor()
   # sqls="INSERT INTO {0} VALUES ({2})".format(tablename,values)

    col = ""
    val = ""
    for k, v in dicts.items():
        col += k + ","
        if type(v) == str:
            val += "'" + str(v) + "',"
        else:
            val += str(v) + ","

    sqls = "INSERT INTO {0} ({1}) VALUES ({2})".format(tablename, col[:-1], val[:-1])


    try:
        cursor.execute(sqls)
        rs=1
    except Exception as e:

        rs=0

    cursor.close()
    return rs

def save_data(tablename,dicts,wheres):
    cursor = connections['default'].cursor()
   # sqls="INSERT INTO {0} VALUES ({2})".format(tablename,values)

    val = ""
    for k, v in dicts.items():

        if type(v) == str:
            val += k + "=" + "'" + str(v) + "',"
        else:
            val += k + "=" + str(v) + ","

    sqls="UPDATE {0} SET {1} WHERE {2}".format(tablename,val[:-1],wheres)



    try:
        cursor.execute(sqls)
        rs = 1
    except Exception as e:
        rs = 0

    cursor.close()
    return rs

def del_data(tablename,wheres):
    cursor = connections['default'].cursor()

    sqls="DELETE FROM {0} WHERE {1}".format(tablename,wheres)

    try:
        cursor.execute(sqls)
        rs = 1
    except Exception as e:
        rs = 0

    cursor.close()
    return rs

def sel_sql(sqlstr):
    cursor = connections['default'].cursor()

    sqls=sqlstr

    cursor.execute(sqls)
    # fetchall返回的是元祖...
    #rs = cursor.fetchall()
    rs=dictfetchall(cursor)
    cursor.close()
    return rs
def sel_field(tablename):
    cursor = connections['default'].cursor()

    sqls=f"select * from {tablename} limit 1"
    cursor.execute(sqls)
    desc = cursor.description
    result=[]
    for i in desc:
        result.append(i[0])

    cursor.close()
    return result
