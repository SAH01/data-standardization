import pymysql
from bs4 import BeautifulSoup
import re
import requests
import lxml
import traceback
import time
import json
from lxml import etree

def get_area(year):
    year=str(year)
    url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/"+ year +"/index.html"
    print(url)
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    response=requests.get(url,headers)
    # print(response.text)
    response.encoding='GBK'
    page_text = response.text
    soup=BeautifulSoup(page_text,'lxml')
    # print(page_text)
    all_province=soup.find_all('tr',class_='provincetr')        #获取所有省份第一级的tr 有4个tr
    # all_province长度为4，其中第一组是从北京市到黑龙江省
    """
    格式是这样的：
    <tr class="provincetr"><td><a href="11.html">北京市<br/></a></td>
    <td><a href="12.html">天津市<br/></a></td>
    <td><a href="13.html">河北省<br/></a></td>
    <td><a href="14.html">山西省<br/></a></td>
    <td><a href="15.html">内蒙古自治区<br/></a></td>
    <td><a href="21.html">辽宁省<br/></a></td><td>
    """
    province_str=""     #为了方便处理，把省份数据变成一个字符串
    for i in range(len(all_province)):
        province_str=province_str+str(all_province[i])
    # print(province_str)
    # 开始分别获得a标签的href和text
    province={}
    province_soup=BeautifulSoup(province_str,'lxml')
    province_href=province_soup.find_all("a")    #获取所有的a标签
    for i in province_href:
        href_str=str(i)
        # print(href_str)
        #创建省份数据字典
        province.update({BeautifulSoup(href_str,'lxml').find("a").text:BeautifulSoup(href_str,'lxml').find("a")["href"]})
    # print(province)
    """
    数据provide字典
    {'北京市': '11.html', '天津市': '12.html', '河北省': '13.html', '山西省': '14.html', 
    '内蒙古自治区': '15.html', '辽宁省': '21.html', '吉林省': '22.html', '黑龙江省': '23.html', 
    '上海市': '31.html', '江苏省': '32.html', '浙江省': '33.html', '安徽省': '34.html', 
    '福建省': '35.html', '江西省': '36.html', '山东省': '37.html', '河南省': '41.html', 
    '湖北省': '42.html', '湖南省': '43.html', '广东省': '44.html', '广西壮族自治区': '45.html',
    '海南省': '46.html', '重庆市': '50.html', '四川省': '51.html', '贵州省': '52.html', '云南省': '53.html',
    '西藏自治区': '54.html', '陕西省': '61.html', '甘肃省': '62.html', '青海省': '63.html', 
    '宁夏回族自治区': '64.html', '新疆维吾尔自治区': '65.html'}
    """
    # 根据身份数据字典继续爬取下一级的市级数据，创建市级数据字典
    city=[]
    city_url=""
    city_tr=[]
    temp_list=[]
    for item in province.items():
        # print(value)
        city_url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/"+year+"/"+item[1]
        city_html=requests.get(city_url,headers)
        city_html.encoding='GBK'
        city_text=city_html.text
        city_tr.append(BeautifulSoup(city_text,'lxml').find_all('tr',class_="citytr"))
        # 获得所有的市区tr city_tr列表长度是31 对应31个省或直辖市
        # 下面开始建立市区的字典{"名字":"链接"}
    #存放省名字列表
    province_key=[]
    for key in province.keys():
        province_key.append(key)
    num=0
    for i in city_tr:
        for j in i:
            # j:<tr class="citytr"><td><a href="11/1101.html">110100000000</a></td><td><a href="11/1101.html">市辖区</a></td></tr>
            # print(j)
            etree_ = etree.HTML(str(j))
            temp_list.append({
                etree_.xpath('//tr/td[2]/a/text()')[0]:
                etree_.xpath('//tr/td[2]/a/@href')[0]
            })
            # print(temp_list)
        city.append({province_key[num]:temp_list})
        num=num+1
        temp_list=[]
    print(len(city))

    """
    city[11]
    {'安徽省': [{'合肥市': '34/3401.html'}, {'芜湖市': '34/3402.html'}, {'蚌埠市': '34/3403.html'}, 
    {'淮南市': '34/3404.html'}, {'马鞍山市': '34/3405.html'}, {'淮北市': '34/3406.html'}, {'铜陵市': '34/3407.html'}, 
    {'安庆市': '34/3408.html'}, {'黄山市': '34/3410.html'}, {'滁州市': '34/3411.html'}, {'阜阳市': '34/3412.html'}, 
    {'宿州市': '34/3413.html'}, {'六安市': '34/3415.html'}, {'亳州市': '34/3416.html'}, {'池州市': '34/3417.html'}, 
    {'宣城市': '34/3418.html'}]}
    """

    # 搞定市级字典，下面开始最后一步，area
    province_name=""
    city_name=""
    area_name=""
    area_tr=[]
    area_list=[]
    temp_area_list=[]

    for item1 in city:
        for k1,v1 in item1.items():
            province_name=k1
            if(province_name in ["北京","天津","上海","重庆"]):
                province_name=province_name+"市"
            if(province_name =="宁夏"):
                province_name=province_name+"回族自治区"
            if(province_name in["西藏","内蒙古"]):
                province_name=province_name+"自治区"
            if(province_name == "新疆"):
                province_name=province_name+"维吾尔自治区"
            if (province_name == "广西"):
                province_name = province_name + "壮族自治区"
            if(province_name=="黑龙江"):
                province_name=province_name+"省"
            if(len(province_name)==2 and province_name not in ["西藏","宁夏","新疆","广西","北京","天津","上海","重庆"]):
                province_name = province_name+"省"
            for item2 in v1:
                for k2,v2 in item2.items():
                    city_name=k2
                    # print(city_name)
                    area_url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/"+ year +"/"+ v2
                    print(area_url)
                    area_response=requests.get(area_url,headers)
                    area_response.encoding='GBK'
                    area_text=area_response.text
                    area_soup=BeautifulSoup(area_text,'lxml')
                    area_tr=area_soup.find_all("tr",class_="countytr")
                    for i in range(len(area_tr)):
                        etree_area = etree.HTML(str(area_tr[i]))
                        try:
                            area_name=etree_area.xpath("//tr/td[2]/a/text()")[0]
                        except:
                            area_name = etree_area.xpath("//tr/td[2]/text()")[0]
                        # print(area_name)
                        # print(str(area_tr[i]))
                        try:
                            temp_area_list.append({
                                etree_area.xpath("//tr/td[1]/a/text()")[0][0:6]: province_name+"·"+city_name+"·"+area_name
                            })
                        except:
                            temp_area_list.append({
                                etree_area.xpath("//tr/td[1]/text()")[0][0:6]: province_name+"·"+city_name+"·"+area_name
                            })
                        area_list.append(temp_area_list)
                        temp_area_list=[]
        time.sleep(1)
    return area_list

def into_mysql(year):
    year=str(year)
    SQL=""
    conn,cursor=get_mysql_conn()
    res=get_area(year)
    try:
        for item in res:
            for k,v in item[0].items():
                print(k)
                print(v)
                SQL="insert into std_area (year,area_code, area_name) values ('"+year+"','"+k+"','"+v+"')"
                print(SQL)
                cursor.execute(SQL)
                conn.commit()
    except:
        print("出现错误")
    conn,cursor.close()
    return None

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
if __name__ == '__main__':
    # res=get_area()
    into_mysql('2009')