import json

from pymongo import MongoClient

#-*- coding:utf-8 -*-

import pymongo

# 链接本地客户端
def get_conn():
    client = MongoClient(host='localhost', port=27017)
    db = client.myDB
    # db = client.get_database("myDB")
    return db
def insert():
    db=get_conn()
    col = db.get_collection("myCollection")    #建表
    post_data = {
        '_id': '10',
        '_item': 'book1',
        '_num': 18}
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
def query():
    db=get_conn()
    col=db.get_collection("myCollection")
    res=col.find_one({'_item' : 'book1'})
    print(res)
    return  None
def update():
    db=get_conn()
    col=db.get_collection("myCollection")
    target={"_item":"book1"}
    new={'pty': 22}
    result = col.update(target, new)
    return result
if __name__ == '__main__':
    # get_conn()
    # insert()
    # query()
    print(update())