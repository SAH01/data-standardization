import pandas as pd
import pymysql
import xlwt


def get_conn():
    """
    获取连接和游标
    :return:
    """
    conn=pymysql.connect(host="127.0.0.1",
                         user="root",
                         password="000429",
                         db="data_cleaning",
                         charset="utf8")
    cursor=conn.cursor()
    return conn,cursor

def close_conn(conn, cursor):
    """
    关闭连接和游标
    :param conn:
    :param cursor:
    :return:
    """
    if cursor:
        cursor.close()
    if conn:
        conn.close()
#query
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
#----------------------------------------------------------------------
def get_excel():
    conn, cursor = get_conn()  # 连接mysql
    if (conn != None):
        print("数据库连接成功！")
    df=pd.read_excel("questionnaire.xlsx")
    #输出测试
    # print(df)
    #输出列名
    """
    ['name' 'college' 'major' 'tel' 'sex' 'grade' 'subject3' 'subject4'
    'subject5' 'subject6' 'subject7']
    """
    # print(df.columns.values)
    #输出具体行列测试
    # print(df.loc[0].values)
    #输出几行几列测试 0:0,0:0
    # print(df.loc[0:,].values)       #['李冠楠' '土木' '土木' '#' 'B' 'B' 'AB' 'ACD' 'D' 'A' 'ABD']
    #遍历表格存入MySQL数据库
    print("表格共有数据:\n",len(df.index.values))
    for i in range(len(df.index.values)):
        print(df.loc[i].values)         #['李冠楠' '土木' '土木' '#' 'B' 'B' 'AB' 'ACD' 'D' 'A' 'ABD']
        SQL="insert into questionnaire values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(df.loc[i].values[0],
                df.loc[i].values[1],
                df.loc[i].values[2],
                df.loc[i].values[3],
                df.loc[i].values[4],
                df.loc[i].values[5],
                df.loc[i].values[6],
                df.loc[i].values[7],
                df.loc[i].values[8],
                df.loc[i].values[9],
                df.loc[i].values[10])
        try:
            cursor.execute(SQL,values)  # 执行sql语句
            conn.commit()  # 提交事务
            print("插入成功:\n", df.loc[i].values[0],"，第"+str(i+1)+"条数据！")
            print("--------------------------------------------------")
        except:
            print("插入失败:\n", df.loc[i].values[0])
    return None

if __name__ == '__main__':
    get_excel()
