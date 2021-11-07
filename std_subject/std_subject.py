import pandas as pd
import pymysql


def get_subject_1992():
    res={}
    the_former_code = ""
    layer1_code = ""  # 一位
    layer1_name = ""
    layer2_code = ""  # 三位
    layer2_name = ""  # 三位
    layer3_code = ""  # 五位
    layer3_name = ""
    layer4_code = ""  # 七位
    layer4_name = ""  # 七位
    df = pd.read_excel("std_subject_1992.xlsx")
    for i in range(len(df.values)):
        item=df.values[i]
        # print(item[0],item[1])
        if (len(str(item[0])) == 1):
            layer1_code = str(item[0])
            layer1_name = item[1]
            # print(layer1_code,layer1_name)
        if (len(str(item[0])) == 3):
            layer2_code = str(item[0])
            layer2_name = item[1]
            # print(layer2_code, layer2_name)
        if (len(str(item[0])) == 5):
            layer3_code = str(item[0])
            layer3_name = item[1]
            if(i!=(len(df.values)-1)):
                if(len(str(df.values[i+1][0]))!=7):
                    # print(layer1_code + layer3_code,layer1_name + "·" + layer2_name + "·" +layer3_name)
                    res.update({layer1_code + layer3_code+"00":layer1_name + "·" + layer2_name + "·" +layer3_name})
            # print(layer3_code, layer3_name)
        if (len(str(item[0])) == 6):
            layer4_code = str(item[0])+"0"
            layer4_name = item[1]
            # print(layer4_code, layer4_name)
            if (layer4_code[:5] == layer3_code):
                # print(layer1_code + layer4_code,layer1_name + "·" + layer2_name + "·" + layer3_name + "·" + layer4_name)
                res.update({layer1_code + layer4_code:layer1_name + "·" + layer2_name + "·" + layer3_name + "·" + layer4_name})
        if (len(str(item[0])) == 7):
            layer4_code = str(item[0])
            layer4_name = item[1]
            # print(layer4_code, layer4_name)
            if (layer4_code[:5] == layer3_code):
                # print(layer1_code + layer4_code,layer1_name + "·" + layer2_name + "·" + layer3_name + "·" + layer4_name)
                res.update({layer1_code + layer4_code:layer1_name + "·" + layer2_name + "·" + layer3_name + "·" + layer4_name})
    return res

"""
---------------------------------------------------------------------------------------
"""
def get_subject_2009():
    res={}
    the_former_code = ""
    layer1_code = ""  # 一位
    layer1_name = ""
    layer2_code = ""  # 三位
    layer2_name = ""  # 三位
    layer3_code = ""  # 五位
    layer3_name = ""
    layer4_code = ""  # 七位
    layer4_name = ""  # 七位
    df = pd.read_excel("std_subject_2009.xlsx")
    for i in range(len(df.values)):
        item=df.values[i]
        # print(item[0],item[1])
        if (len(str(item[0])) == 1):
            layer1_code = str(item[0])
            layer1_name = item[1]
            # print(layer1_code,layer1_name)
        if (len(str(item[0])) == 3):
            layer2_code = str(item[0])
            layer2_name = item[1]
            # print(layer2_code, layer2_name)
        if (len(str(item[0])) == 5):
            layer3_code = str(item[0])
            layer3_name = item[1]
            if(i!=(len(df.values)-1)):
                if(len(str(df.values[i+1][0]))!=7):
                    # print(layer1_code + layer3_code,layer1_name + "·" + layer2_name + "·" +layer3_name)
                    res.update({layer1_code + layer3_code+"00":layer1_name + "·" + layer2_name + "·" +layer3_name})
        if (len(str(item[0])) == 7):
            layer4_code = str(item[0])
            layer4_name = item[1]
            # print(layer4_code, layer4_name)
            if (layer4_code[:5] == layer3_code):
                # print(layer1_code + layer4_code,layer1_name + "·" + layer2_name + "·" + layer3_name + "·" + layer4_name)
                res.update({layer1_code + layer4_code:layer1_name + "·" + layer2_name + "·" + layer3_name + "·" + layer4_name})
    return res
"""
---------------------------------------------------------------------------------------------------------------
"""
def get_conn():
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


def into_mysql():
    global conn, cursor
    res=get_subject_2009()
    for k,v in res.items():
        print(k,v)
        try:
            conn,cursor=get_conn()
            SQL="insert into std_subject_2009 (year,subject_code,subject_name) values (2009,'"+k+"','"+v+"')"
            cursor.execute(SQL)
            conn.commit()
        except:
            print(k,v+" 插入失败！")
    conn,cursor.close()
    return None
if __name__ == '__main__':
    into_mysql()