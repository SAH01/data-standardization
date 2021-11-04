import pandas as pd
import pymysql
from pymongo import MongoClient

def query(sql,*args):
    """
    通用封装查询
    :param sql:
    :param args:
    :return:返回查询结果 （（），（））
    """
    conn , cursor= get_mysql_conn()
    print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    close_conn(conn , cursor)
    return res
"""
------------------------------------------------------------------------------------
"""
def get_mysql_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="000429",
                    db="data_cleaning",
                    charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

# 连接本地客户端
def get_mongo_conn():
    client = MongoClient(host='localhost', port=27017)
    db = client.MyMongoDB
    return db
def insert(post_data,collection):
    db=get_mongo_conn()
    col = db.get_collection(collection)    #建表
    result1 = col.insert_one(post_data)
    # post_1 = {
    #     '_id': '11',
    #     'item1': 'book1',
    #     'qty': 18
    # }
    # post_2 = {
    #     '_id': '12',
    #     'item1': 'book1',
    #     'qty': 18
    # }
    # post_3 = {
    #     '_id': '13',
    #     'item1': 'book1',
    #     'qty': 18
    # }
    #
    # result2 = coll.insert_many([post_1, post_2, post_3])

"""
读文件->存到数据库Mongodb
"""
def into_mongo_0():
    df = pd.read_csv("result.csv")
    # print(df)
    #查看第一行数据
    # print(df.loc[0].values)
    res_dict={}
    for i in range(len(df.index.values)):
        # print(df.loc[i].values)
        #全部转化字符串
        temp0=str(df.loc[i].values[0])
        temp1=str(df.loc[i].values[1])
        temp2=str(df.loc[i].values[2])
        temp3=str(df.loc[i].values[3])
        temp4=str(df.loc[i].values[4])
        temp5=str(df.loc[i].values[5])
        res_dict={"ip":temp0,
                  "time":temp1,
                  "day": temp2,
                  "traffic":temp3,
                  "type":temp4,
                  "id":temp5
                  }
        insert(res_dict)
        print(res_dict)
    return None

def into_mysql():
    """
    清洗：10/Nov/2016:00:01:02 -> 2016-11-10 00:01:02
    :return:
    """
    conn,cursor=get_mysql_conn()
    if(conn!=None):
        print("MySQL数据库连接成功！")
    df = pd.read_csv("result.csv")
    for i in range(len(df.index.values)):
        # print(df.iloc[i].values)
        # 全部转化字符串
        temp0 = str(df.loc[i].values[0])
        temp1 = df.loc[i].values[1][-14:-6]
        res_temp1="2016-11-10 "+temp1
        # print(res_temp1)
        # print(temp1)
        temp2 = str(df.loc[i].values[2])
        temp3 = str(df.loc[i].values[3])
        temp4 = str(df.loc[i].values[4])
        temp5 = str(df.loc[i].values[5])
        SQL="insert into mongo_data (ip,time,day,traffic,type,id) values('"+temp0+"','"+res_temp1+"','"+temp2+"','"+temp3+"','"+temp4+"','"+temp5+"');"
        print(SQL)
        cursor.execute(SQL)
        conn.commit()
    close_conn(conn,cursor)
    return None

def into_mongo_1():
    df = pd.read_csv("result.csv")
    dict={}
    for i in range(len(df.index.values)):
        # print(df.iloc[i].values)
        # 全部转化字符串
        temp0 = str(df.loc[i].values[0])
        temp1 = df.loc[i].values[1][-14:-6]
        res_temp1="2016-11-10 "+temp1
        # print(res_temp1)
        # print(temp1)
        temp2 = str(df.loc[i].values[2])
        temp3 = str(df.loc[i].values[3])
        temp4 = str(df.loc[i].values[4])
        temp5 = str(df.loc[i].values[5])
        dict={"ip":temp0,
                  "time":res_temp1,
                  "day": temp2,
                  "traffic":temp3,
                  "type":temp4,
                  "id":temp5
                  }
        print(dict)
        insert(dict)
    return None

def ques(sql):
    conn,cursor=get_mysql_conn()
    SQL=sql

    res=query(sql)
    dict={}
    for i in res:
        dict={"type":i[0],"id":i[1],"count_id":i[2]}
        print(dict)
        insert(dict,"data1")
    close_conn(conn,cursor)
if __name__ == '__main__':
    # sql="select * from data_1"
    #   select * from data_00
    # ques(sql)
    print()