from sklearn.datasets import load_iris
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import jieba
import pandas as pd
#入门认识
def datasets_demo():
    """
    sklearn数据集使用
    :return:
    """
    # 获取数据集
    # 获取鸢尾花数据集
    iris = load_iris()
    # print(type(iris))
    # print("鸢尾花数据集的返回值：\n", iris)
    # print("-----------------------------------")
    # print("鸢尾花的特征值:\n", iris["data"])
    # print("-----------------------------------")
    # print("鸢尾花的目标值：\n", iris.target)
    # print("-----------------------------------")
    # print("鸢尾花特征的名字：\n", iris.feature_names)
    # print("-----------------------------------")
    # print("鸢尾花目标值的名字：\n", iris.target_names)
    # print("-----------------------------------")
    # print("鸢尾花的描述：\n", iris.DESCR)
    # 2、对鸢尾花数据集进行分割

    # 训练集的特征值x_train 测试集的特征值x_test 训练集的目标值y_train 测试集的目标值y_test
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=22)
    print("x_train:\n", x_train.shape)
    # 随机数种子
    x_train1, x_test1, y_train1, y_test1 = train_test_split(iris.data, iris.target, random_state=6)
    x_train2, x_test2, y_train2, y_test2 = train_test_split(iris.data, iris.target, random_state=6)
    print("如果随机数种子不一致：\n", x_train == x_train1)
    print("如果随机数种子一致：\n", x_train1 == x_train2)
    return None

#字典特征提取
"""
应用场景：
1、数据集当中类别特征比较多
2、本身数据集就是字典类型

把字典里的类别转化为 one-hot编码
"""
def dict_deme():
    data =[{'city': '北京','temperature':100},{'city': '上海','temperature':60},{'city': '深圳','temperature':30}]

    #1、实例化一个转换器类
    transfer = DictVectorizer(sparse=False)
    #2、调用fit_transfer() 默认返回稀疏矩阵
    data_new = transfer.fit_transform(data)
    print("data_new:")
    print(data_new)
    print("特征名字:", transfer.get_feature_names_out())
    return None

"""
    英文文本特征抽取
    1、总结出分词字段组，文本特征
    2、根据文本特征名字，找出每个字段中某个文本特征名字出现的次数
"""
def count_demo():
    #文本特征抽取，CountVectorizer
    data= ["stay hungry,","stay foolish.","good good good."]
    #实例化一个CountVectorizer
    transfer=CountVectorizer()
    #调用
    data_new=transfer.fit_transform(data)
    print(data_new.toarray())
    print("文本特征名字:", transfer.get_feature_names_out())
    return None


"""
    中文文本特征抽取
"""
def count_chinese_demo():
    # 文本特征抽取，CountVectorizer
    data = ["高筑墙", "广积粮", "缓称王"]
    # 实例化一个CountVectorizer
    transfer = CountVectorizer()
    # 调用
    data_new = transfer.fit_transform(data)
    print(data_new.toarray())
    print("中文文本特征名字:", transfer.get_feature_names_out())
    return None

"""
    中文文本特征抽取(结巴分词)
"""
def count_chinese_demo2():
    # 文本特征抽取，CountVectorizer
    data=["今天很残酷，明天更残酷，后天很美好，但绝对大部分是死在明天晚上，所以每个人不要放弃今天。",
          "我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去。",
          "如果只用一种方式了解某样事物，你就不会真正了解它。了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系。"]
    #中文文本进行分词

    # ['今天 很 残酷 ， 明天 更 残酷 ， 后天 很 美好 ， 但 绝对 大部分 是 死 在 明天 晚上 ，
    # 所以 每个 人 不要 放弃 今天 。', '我们 看到 的 从 很 远 星系 来 的 光是在 几百万年 之前 发出 的 ， 这样 当 我们 看到 宇宙 时 ，
    # 我们 是 在 看 它 的 过去 。', '如果 只用 一种 方式 了解 某样 事物 ， 你 就 不会 真正 了解 它 。
    # 了解 事物 真正 含义 的 秘密 取决于 如何 将 其 与 我们 所 了解 的 事物 相 联系 。']
    data_final = []
    for data_part in data:
        data_final.append(cut_word(data_part))
    print(data_final)
    # 实例化一个CountVectorizer
    transfer = CountVectorizer()
    # 调用
    data_new = transfer.fit_transform(data_final)
    print(data_new.toarray())
    print("中文文本特征名字:", transfer.get_feature_names_out())

    return None

#结巴分词函数
def cut_word(text):
    """
    进行中文分词
    传入一个中文字符串
    返回一个词语生成器
    :param text:
    :return:
    """
    cut_text= " ".join(jieba.cut(text))
    # print(type(cut_text))
    # print(cut_text)
    return cut_text

#TF-IDF
"""
词频（term frequency，tf）指的是某一个给定的词语在该文件中出现的频率
逆向文档频率（inverse document frequency，idf）是一个词语普遍重要性的度量。某一特定词语的idf，可以由总文件数目除以包含该词语之文件的数目，
再将得到的商取以10为底的对数得到
"""
def tfidf_demo():
    """
    用TF-IDF的方法进行文本特征抽取
    :return:
    """
    data = ["今天很残酷，明天更残酷，后天很美好，但绝对大部分是死在明天晚上，所以每个人不要放弃今天。",
            "我们看到的从很远星系来的光是在几百万年之前发出的，这样当我们看到宇宙时，我们是在看它的过去。",
            "如果只用一种方式了解某样事物，你就不会真正了解它。了解事物真正含义的秘密取决于如何将其与我们所了解的事物相联系。"]
    # 中文文本进行分词
    # ['今天 很 残酷 ， 明天 更 残酷 ， 后天 很 美好 ， 但 绝对 大部分 是 死 在 明天 晚上 ，
    # 所以 每个 人 不要 放弃 今天 。', '我们 看到 的 从 很 远 星系 来 的 光是在 几百万年 之前 发出 的 ， 这样 当 我们 看到 宇宙 时 ，
    # 我们 是 在 看 它 的 过去 。', '如果 只用 一种 方式 了解 某样 事物 ， 你 就 不会 真正 了解 它 。
    # 了解 事物 真正 含义 的 秘密 取决于 如何 将 其 与 我们 所 了解 的 事物 相 联系 。']
    data_final = []
    for data_part in data:
        data_final.append(cut_word(data_part))
    print(data_final)
    # 实例化一个TfidfVectorizer
    transfer = TfidfVectorizer()
    # 调用
    data_new = transfer.fit_transform(data_final)
    print(data_new.toarray())
    print("TF-IDF中文文本特征名字:", transfer.get_feature_names_out())
    return None
"""
    特征预处理
    1、归一化
    2、标准化
"""
def minmax():
    """
    归一化
    :return:
    """
    #1、获取数据
    data=pd.read_csv("dating.txt")
    print("dating:")
    # print(data)
    data= data.iloc[:,:3]
    # print(data)

    #2、获取转换器
    transfer=MinMaxScaler()
    #3、调用fit_transform进行转化
    data_new = transfer.fit_transform(data)
    print("data_new:\n",data_new)
    return data_new

"""
标准化
"""
def stand_demo():
    """
    标准化演示
    :return: None
    """
    data = pd.read_csv("dating.txt")
    print(data)
    # 1、实例化一个转换器类
    transfer = StandardScaler()
    # 2、调用fit_transform
    data = transfer.fit_transform(data[['milage','Liters','Consumtime']])
    print("标准化的结果:\n", data)
    print("每一列特征的平均值：\n", transfer.mean_)
    print("每一列特征的方差：\n", transfer.var_)

    return None
if __name__ == '__main__':
    # datasets_demo()
    #1 字典提取
    # dict_deme()
    #2 文本提取
    # count_demo()
    #3 中文提取
    # count_chinese_demo()
    #4 结巴分词提取中文
    # count_chinese_demo2()
    #5 测试结巴分词函数
    # cut_word("我爱北京天安门")
    #6 TF-IDF
    #7 tfidf_demo()
    #8 归一化
    #minmax()
    #9 标准化
    stand_demo()