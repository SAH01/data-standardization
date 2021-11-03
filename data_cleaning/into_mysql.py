import pandas as pd
import pymysql
"""
------------------------------------------------------------------------------------
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
"""
-----------------------------------------------------------
"""
"""
------------------------------------------------------------------------------------
"""
def query(sql,*args):
    """
    通用封装查询
    :param sql:
    :param args:
    :return:返回查询结果 （（），（））
    """
    conn , cursor= get_conn()
    print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    close_conn(conn , cursor)
    return res
"""
------------------------------------------------------------------------------------
"""
count=0     #计算四位编码个数
def into_mysql(*filename):
    category_code = ""      #门类编码
    category_name = ""      #门类名称
    global count
    conn,cursor=get_conn()  #连接mysql
    if(conn!=None):
        print("数据库连接成功！")
    print(filename)
    for file in filename:               #三个文件
        print(file)
        tempres = []                #暂存列表
        df=pd.read_excel(file)      #读取标准表
        print(len(df.index))
        for i in range(len(df.index.values)):   #第一层遍历标准表 找到门类的编码和名称 找到小类的编码
            # print(df.loc[i][1])
            code=str(df.loc[i][0])           #所有的编码
            name=str(df.loc[i][1])           #所有的名称
            if len(code)==1:
                category_code=code     #门类编码
                category_name=name     #门类名称
            #分割编码
            if len(code)==4:
                count=count+1
                small_class=name        #小类名称
                new_code_2=code[:2]     #分割出两位编码    之后确定大类名称
                new_code_3=code[:3]     #分割出三位编码    之后确定中类名称
                print(file[8:12])
                print(category_code)    #最终的字符串需要门类的编码ABCD和门类的名称
                print(new_code_2)
                print(new_code_3)
                for j in range(len(df.index.values)):   #第二次遍历 寻找不同的位数的编码对应不同的名称
                    if new_code_2==df.loc[j][0]:
                        big_class=df.loc[j][1]    #大类名称
                    if new_code_3==df.loc[j][0]:
                        mid_class=df.loc[j][1]    #中类名称
                tempres.append(code)                            #列表暂存0511 编码
                tempres.append(category_code+code)              #列表暂存A0511 编码
                tempres.append(category_name+"·"+big_class+"·"+mid_class+"·"+small_class)   #列表暂存完整的名称
                print(tempres)
                #====================================================================================
                SQL = "insert into std_code (year,code_0,code,name) values('"+file[8:12]+"','"+tempres[0]+"','"+tempres[1]+"','"+tempres[2]+"');"     #sql插入语句
                cursor.execute(SQL)             #执行sql语句
                conn.commit()                   #提交事务
                print("--------------------------------------------------")
                # ====================================================================================
                tempres=[]          #清空列表
    close_conn(conn,cursor)     #关闭数据库连接
    print("所有的四位编码数：\n",count)
    return None
if __name__ == '__main__':
    #913    1094    1377    共3384
    into_mysql("GBT4754-2002.xlsx","GBT4754-2011.xlsx","GBT4754-2017.xlsx")