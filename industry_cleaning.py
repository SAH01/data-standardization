import pandas as pd
import xlwt
rank10=""    #A
rank11=""    #A的名字
rank20=""
rank21=""
rank30=""
rank31=""
rank40=""
rank41=""
finalstr=""
def std_excel():
    # dict={"A":{"01":{"011":"谷物种植","0111":"稻谷种植"} ,
    #            "02":{"021":"林木育种和育苗","0211":"林木育种"}},
    #
    #       "B":{"06":{ "0610":"烟煤和无烟煤开采洗选","0620":"褐煤开采洗选"},
    #            "07":{"0710":"石油开采","0720":"天然气开采"}}
    #       }

    # layer1=dict['A']
    # print("第一层 A：\n",layer1)
    #
    # layer2 = dict['A']['01']
    # print("第二层 01农业：\n", layer2)
    #
    # layer3 = dict['A']['01']["011"]
    # print("第三层 ：\n", layer3)
    #读取标准文件
    df = pd.read_excel('GBT4754-2011.xlsx')
    #首先寻找第一层大写字母层的数据 定位行loc[] 定位
    # print(df.columns.values[0]) #A
    my_dict={"A":{}}
    new_dict={"A":
                  {"农、林、牧、渔业":
                       {"01":
                            {"农业":
                                 {"001":
                                      {"谷物种植":
                                          {
                                            "0111":"稻谷种植","0112":"小麦种植"
                                          }
                                       }
                                  }
                             }
                        }
                   }
              }
    # new_dict["A"].update(
    #     {df.loc[0].values[0]:df.loc[0].values[1]}
    # )
    # print("excel表的行数：\n",len(df.index.values))
    # print("测试字典：\n",new_dict)
    # print(df.loc[80].values)
    # print("一个单元格数据的数据类型：\n",type(df.loc[0].values[0]))

    #测试完毕 开始构建行业领域分类字典
    industry_json={}
    #开始遍历表格 0 - 1423
    for i in range(len(df.index.values)):
        #由于表格的第一列数据被判定为int型 所以要转化成str
        temp=df.loc[i].values
        one = str(temp[0])
        # print(len(one))
        two = str(temp[1])
        # print("数据格式：\n",type(temp[0]))
        #通过判断values[0]的字符串的长度判断处于字典的哪一层 如果长度是1 那么在第一层门类 如果长度是2那么在第二层大类 如果长度是3那么在第三层中类
        if(len(one)==1):
            global rank10
            global rank11
            rank10=one
            rank11=two
            my_dict.update({rank10:{rank11:{}}})
        if(len(one)==2):
            global rank20
            global rank21
            rank20 = one
            rank21 = two
            my_dict[rank10][rank11].update({rank20:{rank21:{}}})
        if (len(one) == 3):
            global rank30
            global rank31
            rank30 = one
            rank31 = two
            my_dict[rank10][rank11][rank20][rank21].update({rank30:{rank31:{}}})
        #这里做了代码的前三位字符串切分，为了判断一下有没有小类跳过中类的情况，需要直接跨过中类存储，少了一层字典{}
        if (len(one) == 4):
            global rank40
            global rank41
            rank40 = one
            rank41 = two
            divide_rank40=rank40[:3]
            # print(divide_rank40,rank30)
            if(divide_rank40==rank30):
                # print("!!!!!~~~~~~~~~~~~")
                my_dict[rank10][rank11][rank20][rank21][rank30][rank31].update({rank40:rank41})
            else:
                my_dict[rank10][rank11][rank20][rank21].update({rank40: rank41})
    #得到最终的字典my_dict
    # print(my_dict.keys())
    # print(my_dict)
    return my_dict
def is_excit(qb03):
    global finalstr
    #设置个标记，初始值False 说明默认找不到这个编码 如果找到了则设为 True 如果最终是False则重新分割字符串回调函数
    flag = False
    #获取字典
    my_dict={}
    my_dict.update(std_excel())
    # print(my_dict)
    #门类KEY
    category=""
    #大类
    big_class=""
    #中类
    medium_class=""
    #小类
    small_class=""
    # 遍历第一层 门类

    for items in my_dict.items():
        res = ""
        for layer_0 in items[1].items():
            # print("门类：\n",layer_0)
            # print("门类名称:\n",layer_0[0])
            category=layer_0[0]
            """
            --------------------------------------------------
            """
            # 遍历第二层大类
            """
            每进入一层遍历第一个for循环是进入一个这样格式的数据 （ 编码：{  } ）
            之后第二个for循环进入那个字典{ }
            字典构建的方式是 上一层是key 下一层是对应的value 同时它作为下一层的key
            
            """
            #进入第一层（A：{ } ）
            for layer_10 in layer_0[1].items():
                # print("大类编码（两位）：\n",layer_10[0])
                #进入A对应的{ }
                for layer_11 in layer_10[1].items():
                    # print("大类：\n",layer_11)
                    big_class = layer_11[0]
                    # 自己调用自己补全缺失值
                    if(len(qb03)==2 and qb03==layer_10[0]):
                        print("缺失值补全：\n", finalstr)
                        flag=True
                        res = finalstr + "·" + category + "·" + big_class + "·" + big_class + "·" + big_class
                        # print(res)
                        return res
                    # print("大类名称：\n",big_class)
                    """
                    --------------------------------------------------
                    """
                    #进入大类（01，{ }）
                    for layer_20 in layer_11[1].items():
                        #进入01对应的 { }
                        #判断第二层下一级的名称是三位还是四位，如果是三位那么是正常的中类划分，如果是四位，那么是跳过了中类划分到了小类
                        if(len(layer_20[0])==4):
                            small_class=layer_20[1]
                            # print("大类直接分到小类：\n",small_class)
                            #判断字符串
                            if(qb03==layer_20[0]):
                                print("跨过中类的小类，判断成功！",qb03)
                                flag=True
                                res = qb03+ "·"+ category + "·" + big_class + "·"+small_class+ "·"+small_class
                                return res
                        else:
                            #这个分支的意思是有的类别只到了大类，没有中类直接分到了四位数的小类，所以必须分开遍历，字符串不能按字典遍历
                            for layer_21 in layer_20[1].items():
                                # print("中类：\n",layer_21)
                                medium_class = layer_21[0]
                                # print("中类名称:\n",medium_class)
                                # 这里是个大坑，我的遍历是进入值的那一层，编码在上一级的遍历 layer_20[0]
                                if (qb03 == layer_20[0]):
                                    print("三位中类判断成功！", qb03)
                                    flag=True
                                    res = qb03 + "·" + category + "·" + big_class + "·" + medium_class+ "·" + medium_class
                                    return res
                                #继续划分到小类
                                for layer_30 in layer_21[1].items():
                                    #这个layer_30就是最后一层的四位数数据了 格式： ('0111', '稻谷种植') 是一个tuple 索引0是编码1是名称
                                    small_class=layer_30[1]
                                    # print("小类名称：\n",small_class)
                                    #--------------------------------------------------------------------------------
                                    # 判断字符串
                                    if (qb03 == layer_30[0]):
                                        print("正常四位小类判断成功！", qb03)
                                        flag=True
                                        res=qb03+"·"+category+"·"+big_class+"·"+medium_class+"·"+small_class
                                        return res
    if(flag==False):
        finalstr = qb03
        new_qb03=qb03[:2]
        return is_excit(new_qb03)
def clean():
    """
    1、读取源数据表格
    2、逐个把数据传入is_exist()方法获得返回值存回excel表格
    :return:
    """
    df=pd.read_excel("2013_year_data.xlsx")
    # print(df.loc[0].values)
    res=[]
    temp_res=""
    #range(len(df.index.values))
    for i in range(len(df.index.values)):
        # print(df.loc[i].values[0])
        temp_res=is_excit(str(df.loc[i].values[0]))
        print(temp_res)
        if(temp_res!=None):
            res.append(temp_res)
        else:
            res.append(str(df.loc[i].values[0]))
    # print(res)
    #把结果存储到excel表
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    sheet.col(0).width=256*100
    sheet.write(0, 0, "data")
    for i in range(len(res)):
        sheet.write(i+1, 0, res[i])
    workbook.save('2013_res_data.xls')
    return None
if __name__ == '__main__':
    # print()
    #311 2662 610
    # res=is_excit("610")
    # print("----------------------")
    # print(res)
    # print("----------------------")

    clean()