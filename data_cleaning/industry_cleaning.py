import pandas as pd
import xlwt

"""
rank的一系列变量是生成json字符串需要的标志
由于json结构是循环遍历生成的，所以在每一层都要留下标记，以便于下一层的构建
"""

rank10=""    #A  门类编号
rank11=""    #A  门类名字
rank20=""    #01 大类编号
rank21=""    #   大类名字
rank30=""    #012 中类编号
rank31=""    #    中类名字
rank40=""    #0121小类编号
rank41=""    #    小类名字

"""
------------------------------------------------------------------------------------------------------------------------
"""

def get_json(stdfilepwd):
    """
    :param stdfilepwd:标准国标文件
    :return: 标准行业维度json
    """
    """
    filepwd 国标文件格式
    A	农、林、牧、渔业
    A	农、林、牧、渔业
    01	农业
    011	谷物种植
    0111	稻谷种植
    0112	小麦种植
    0113	玉米种植
    """
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
    #读取标准文件 df默认不读取第一行数据
    df = pd.read_excel(stdfilepwd)
    #首先寻找第一层大写字母层的数据 定位行loc[] 定位
    # print(df.columns.values[0]) #A

    my_dict={"A":{}}                #最终生成的字典
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
    #开始遍历表格 0 - 1423
    for i in range(len(df.index.values)):
        #由于表格的第一列数据的数字被判定为int型 所以要转化成str
        temp=df.loc[i].values
        #转化字符串 为了保险起见 两列统一化处理 均转化为字符串
        # one 就是编码 two就是编码对应的行业名称
        one = str(temp[0])
        # print(len(one))
        two = str(temp[1])
        # print("数据格式：\n",type(temp[0]))
        #通过判断values[0]（数字编码）的字符串的长度判断处于字典的哪一层 如果长度是1 那么在第一层门类 如果长度是2那么在第二层大类 如果长度是3那么在第三层中类
        if(len(one)==1):
            #rank10保存编码 rank11保存行业名称 后面类似
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
            #虽然会出现21 ， 2111 中间没有210的情况出现 但是可以优先生成所有的中类三位数的json结构 这一层会保留最后一个三位数中类 可以在后面进行判断
            my_dict[rank10][rank11][rank20][rank21].update({rank30:{rank31:{}}})
            #这里做了代码的前三位字符串切分，为了判断一下有没有小类跳过中类的情况，需要直接跨过中类存储，少了一层字典{}
        if (len(one) == 4):
            global rank40
            global rank41
            rank40 = one
            rank41 = two
            #把编码分片 只取前三位 然后和距离这个编码最近的那个三位数中类做比较 如果相同则可以放到该中类的下一层字典 如果不同则该四位编码自成一个字典
            divide_rank40=rank40[:3]
            # print(divide_rank40,rank30)
            #判等
            if(divide_rank40==rank30):
                # print("!!!!!~~~~~~~~~~~~")
                #相等 -> 放入该中类的下一层字典
                my_dict[rank10][rank11][rank20][rank21][rank30][rank31].update({rank40:rank41})
            else:
                #不等 -> 自己成为一个字典 在大类里直接自成一个字典
                my_dict[rank10][rank11][rank20][rank21].update({rank40: rank41})
    #得到最终的字典my_dict
    # print(my_dict.keys())
    # print(my_dict)
    return my_dict
"""
最终生成的json文件

'A': {
		'农、林、牧、渔业': {
			'01': {
				'农业': {
					'011': {
						'谷物种植': {
							'0111': '稻谷种植',
							'0112': '小麦种植',
							'0113': '玉米种植',
							'0119': '其他谷物种植'
						}
					},
					'012': {
						'豆类、油料和薯类种植': {
							'0121': '豆类种植',
							'0122': '油料种植',
							'0123': '薯类种植'
						}
					},
					'013': {
						'棉、麻、糖、烟草种植': {
							'0131': '棉花种植',
							'0132': '麻类种植',
							'0133': '糖料种植',
							'0134': '烟草种植'
						}
					},
					'014': {
					
"""


"""
------------------------------------------------------------------------------------------------------------------------
"""

def ger_stdstr(qb03,stdfilepwd):
    """
    :param qb03,stdfilepwd:
    :return: str 标准行业维度字符串 行业代码·门类名称·大类名称·中类名称·小类名称
    qb03,待查编码
    stdfilepwd,标准国标文件
    """
    #设置个标记，初始值False 说明默认找不到这个编码 如果找到了则设为True 如果最终是False则重新分割字符串，回调函数
    flag = False
    #获取字典
    my_dict={}
    my_dict.update(get_json(stdfilepwd))
    # print(my_dict)

    category=""     #门类 名字

    big_class=""    #大类 名字

    medium_class="" #中类 名字

    small_class=""  #小类 名字
    # for 遍历第一层 门类
    for items in my_dict.items():
        res = ""                       #    定义该方法最终要返回的标准化行业维度字符串
        # print(items[0])                 #ABCD
        for layer_0 in items[1].items():                #这个for循环已经进入了 第一层 {} 里面格式是 （门类名称：{ }）
            # print("门类：\n",layer_0)
            # print("门类名称:\n",layer_0[0])
            category=layer_0[0]                         #门类名称[0]
            """
            -------------------------------------------------------------------
            """
            # 遍历第二层大类
            """
            每进入一层遍历，第一个for循环是进入一个这样格式的数据 （ 编码：{  } ） [0]是名称 [1]是字典
            之后第二个for循环进入那个字典{ }
            字典构建的方式是 上一层是key 下一层是对应的value 同时它作为下一层的key
            """
            for layer_10 in layer_0[1].items():
                # print("大类编码（两位）：\n",layer_10[0])
                #进入A对应的{ }
                for layer_11 in layer_10[1].items():        #这个for循环已经进入了 第二层 {} 里面格式是 （大类名称：{ }）
                    # print("大类：\n",layer_11)
                    big_class = layer_11[0]
                    # print("大类名称：\n",big_class)
                    """
                    ---------------------------------------
                    """
                    #进入大类（01，{ }）
                    for layer_20 in layer_11[1].items():#这个for循环已经进入了 第三层 {} 里面格式是 （中类名称：{ }）或者不正常的跨过中类的四位编码
                        # 这个分支的意思是有的类别只到了大类，没有经过中类直接分到了四位数的小类，所以必须分开遍历
                        #判断第二层下一级的编码是三位还是四位，如果是三位那么是正常的中类划分，如果是四位，那么是跳过了中类划分到了小类
                        if(len(layer_20[0])==4):
                            small_class=layer_20[1]
                            # print("大类直接分到小类：\n",small_class)
                            #判断字符串
                            if(qb03==layer_20[0]):
                                print("跨过中类的小类，判断成功！",qb03)
                                flag=True
                                res = items[0]+ qb03+ "·"+ category + "·" + big_class + "·"+small_class
                                return res
                        else:
                            for layer_21 in layer_20[1].items():    #这个for循环已经进入了 第三层正常的中类 {} 里面格式是 （中类名称：{ }）
                                # print("中类：\n",layer_21)
                                medium_class = layer_21[0]
                                # print("中类名称:\n",medium_class)
                                # 这里是个大坑，我的遍历是进入值的那一层，编码在上一级的遍历 layer_20[0]
                                # if (qb03 == layer_20[0]):
                                #     print("三位中类判断成功！", qb03)
                                #     flag=True
                                #     res = qb03 + "·" + category + "·" + big_class + "·" + medium_class
                                #     return res
                                #继续划分到小类
                                for layer_30 in layer_21[1].items():    #这个for循环已经进入了 第四层 {} 里面格式是 （小类名称：{ }）
                                    #这个layer_30就是最后一层的四位数数据了 格式： ('0111', '稻谷种植') 是一个tuple 索引0是编码1是名称
                                    small_class=layer_30[1]
                                    # print("小类名称：\n",small_class)
                                    #--------------------------------------------------------------------------------
                                    # 判断字符串
                                    if (qb03 == layer_30[0]):
                                        print("正常四位小类判断成功！", qb03)
                                        flag=True
                                        res=items[0]+qb03+"·"+category+"·"+big_class+"·"+medium_class+"·"+small_class
                                        return res
    #这里是对没有找到的编码进行二次寻找，字符串拼接，最前面加个0
    if(flag==False):
        new_qb03="0"+qb03
        return ger_stdstr(new_qb03,stdfilepwd)               #递归调用自身

"""
------------------------------------------------------------------------------------------------------------------------
"""

def do_clean(filepwd,newfilepwd,stdfilepwd):
    """
    1、读取源数据表格
    2、逐个把数据传入get_stdstr(qb03,stdfilepwd)方法获得返回值存回excel表格
    参数：需要清洗的行业编码，单列数据
    filepwd,需要清洗的文件
    newfilepwd,新生成的文件存储路径
    stdfilepwd,标准的国标文件
    :return:None
    """
    """
    待清洗的文件格式：filepwd
    QB03
    2812
    3511
    3071
    3434
    2614
    3620
    2613
    2614
    3512
    
    清洗完毕的文件格式：newfilepwd
    data
    2812·制造业·化学纤维制造业·纤维素纤维原料及纤维制造·人造纤维（纤维素纤维）制造
    3511·制造业·专用设备制造业·采矿、冶金、建筑专用设备制造·矿山机械制造
    3071·制造业·非金属矿物制品业·陶瓷制品制造·卫生陶瓷制品制造
    3434·制造业·通用设备制造业·物料搬运设备制造·连续搬运设备制造
    2614·制造业·化学原料和化学制品制造业·基础化学原料制造·有机化学原料制造
    3620·制造业·汽车制造业·改装汽车制造·改装汽车制造
    2613·制造业·化学原料和化学制品制造业·基础化学原料制造·无机盐制造
    2614·制造业·化学原料和化学制品制造业·基础化学原料制造·有机化学原料制造
    3512·制造业·专用设备制造业·采矿、冶金、建筑专用设备制造·石油钻采专用设备制造
    3599·制造业·专用设备制造业·环保、社会公共服务及其他专用设备制造·其他专用设备制造
    511·批发和零售业·批发业·农、林、牧产品批发·农、林、牧产品批发
    3821·制造业·电气机械和器材制造业·输配电及控制设备制造·变压器、整流器和电感器制造
    6520·信息传输、软件和信息技术服务业·软件和信息技术服务业·信息系统集成服务·信息系统集成服务
    7330·科学研究和技术服务业·研究和试验发展·农业科学研究和试验发展·农业科学研究和试验发展
    2922·制造业·橡胶和塑料制品业·塑料制品业·塑料板、管、型材制造
    """
    df=pd.read_excel(filepwd)
    # print(df.loc[0].values)
    res=[]
    temp_res=""
    #range(len(df.index.values))
    for i in range(len(df.index.values)):
        # print(df.loc[i].values[0])
        """
        ger_stdstr()
        两个参数 一个是待查编码   一个是标准json文件路径
        """
        temp_res=ger_stdstr(str(df.loc[i].values[0]),stdfilepwd)
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
    sheet.write(0, 0, "DATA")
    for i in range(len(res)):
        sheet.write(i+1, 0, res[i])
    workbook.save(newfilepwd)
    return None
if __name__ == '__main__':
    #封装方法getjson()
    """
    1、封装构建json的方法 getjson() , 方法有一个参数 参数是文件路径
    文件的格式是两列，由于读取文件不包括表头，如果表头数据有需要的话 需要复制一行表头数据
    第一列是行业编码 第二列是行业名称
    """
    #测试调用
    stdfilepwd="GBT4754-2011.xlsx"
    # get_json(stdfilepwd)
    """
    --------------------------------------------------------------
    """
    #封装方法do_clean(filepwd,newfilepwd,stdfilepwd)
    # 测试调用
    filepwd="2013_year_data.xlsx" #需要处理的文件路径13年
    newfilepwd="2013_res_data.xls"  #处理完毕转存的文件路径13年
    filepwd16 = "2016_year_data.xlsx"  # 需要处理的文件路径16年
    newfilepwd16 = "2016_res_data.xls"  # 处理完毕转存的文件路径16年
    do_clean(filepwd16, newfilepwd16, stdfilepwd)
    """
    --------------------------------------------------------------
    """
    #封装ger_stdstr(qb03,jsonfilepwd) 方法   参数1是四位待查编码  参数2是json文件的路径
    # res=ger_stdstr("321",stdfilepwd)
    # print(res)
