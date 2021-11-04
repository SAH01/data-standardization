from pymongo import MongoClient
# 向文件中插入数据
client=MongoClient(host='localhost',port=27017)
db=client.get_database('myDB')
my_infor=db.get_collection("myCollection")
user = [{'name':'jiesen','age':15,'sex':'男'},{'name':'jiesen','age':35,'sex':'男'},{'name':'jiesen','age':23,'sex':'男'}]
# my_infor.insert_many(user)
'''
insert():可以实现单条或多条数据的插入
save():只能完成单条数据的插入,并且数据必须是字典结构
'''

# 查询数据
res = my_infor.find({'name':'jiesen'})
# for item in res:
#     print(item)

# 更新数据
# multi: 布尔类型, 设置数据更新时是否一次性更新多条数据, 默认为False
# upsert: 设置数据更新时,如果数据不存在,是否将本次数据添加到文件中,默认为False
my_infor.update({'name':'jiesen1'},{'$set':{'age':20,'sex':'woman'}},multi=True,upsert=True)

# 删除数据
# delete_one(): 删除数据中一条数据
# delete_many(): 一次性删除多条满足的数据
# my_infor.delete_many({'name':'jiesen'})

# mongodb条件查询:
'''
> : $gt
< : $lt
>= : $gte
<= : $lte
$in:(m,n,) : 提取在指定内容中的数据

$all[n,m,...]: 查找数据库中某一条数据是否全部包含all中的数据, 如果'全部'包含则返回该条数据,否则不反悔

$push: 向已有数据源中按照字段进行数据的添加.基于'列表'

$pop: 将数据库中对应数据的某一个字段数据按照指定方式进行删除. 其中 -1:从列表的起始位置开始删除; 1: 从列表的最后位置开始删除

$pull: 将对应数据中指定的数据分布进行删除(按值删除)

$or : 或者指令, 该指令通常作为字典的键, 其对应的值是一个'列表'结构,列表中每一个元素之间是'并列'的关系.

"在字典中所有的键值对之间代表的是一种'并且'的关系."

.sort('age',1): 将查找之后的结果按照指定的字段进行排序, 1为升序,-1为降序

.skip(m).limit(n): 将查找结果的取值显示为,跳过m条数据,显示n条数据.  即只显示m+1~m+1+n的数据
'''
#例:
#查询年龄在[5,25]之间的所有数据
res = my_infor.find({
    'age':{'$gte':5,"$lte":25}
})
# for item in res:
#     print(item)

#查询年龄15以下或25以上,name是jiesen的数据
res1 = my_infor.find({
    '$or':[
        {'age':{'$gte':25}},
        {'age':{'$lte':15}}
    ],
    'name':'jiesen'
})


# $in: 提取在指定内容中的数据
res3 = my_infor.find({
    'age':{'$in':(15,23)}
})

obj = {
    'name':'ysh',
    'sex':'男',
    'age':77,
    'photo':['img/1.jpg','img/2.jpg'],
    'score':[12,15,17,90]
}
# my_infor.insert(obj)

res4 = my_infor.find({
    'score':{'$all':[12,15,90]}
})

# $push: 向已有数据源中按照字段进行数据的添加.基于'列表'
# my_infor.update(
#     {'name':'ysh'},   #指定数据的条件
#     {'$push':{'score':[103,120]}}
# )

# $pop: 将数据库中对应数据的某一个字段数据按照指定方式进行删除. 其中 -1:从列表的起始位置开始删除; 1: 从列表的最后位置开始删除
# $pull: 将对应数据中指定的数据分布进行删除(按值删除)
my_infor.update(
    {'name':'ysh'},
    # {'$pop':{'score':1}},
    {'$pull':{'score':90}}
)

#多路查询
res5 = my_infor.find({
    'score.0':{'$gt':10}
})

obj1 = {
    'name':'YSH',
    'son':[
        {'name':'ete','age':17},
        {'name':"ete1",'age':15}
    ]
}
# my_infor.insert(obj1)
res6 = my_infor.find({
    'son.1.age':15
})
for item in res6:
    print(item)
