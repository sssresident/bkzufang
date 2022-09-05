# coding=utf-8
import pandas as pd
import numpy as np

if __name__ == '__main__':


    #获取data目录下的csv文件的
    df=pd.read_csv(r"data.csv",encoding="gbk")
    #print(df)
    #各区分类汇总
    areagroup=dict(df.groupby('行政区').size())

    # 户型分类汇总top10
    housetype = dict(df.groupby('户型').size())
    housetype=sorted(housetype.items(), key=lambda kv: (kv[1]),reverse=True)

    #各区平均月租
    rent=dict(df.groupby('行政区').agg({'月租': np.average}))
    rent=dict(rent['月租'])
    for k,v in rent.items():
        rent[k]=int(v)
    rent = sorted(rent.items(), key=lambda kv: kv[1], reverse=True)
    #print(rent)

    m0_50=df[(df.面积>0) & (df.面积 <=50)]
    m50_100 = df[(df.面积 > 50) & (df.面积 <= 100)]
    m100_150 = df[(df.面积 > 100) & (df.面积 <= 150)]
    m150 = df[(df.面积 > 150) & (df.面积 <= 9999999)]

    m0_50g=dict(m0_50.groupby('行政区').size())
    m50_100g = dict(m50_100.groupby('行政区').size())
    m100_150g = dict(m100_150.groupby('行政区').size())
    m150g = dict(m150.groupby('行政区').size())
    print(m0_50g)
    print(m50_100g)
    print(m100_150g)
    print(m150g)








