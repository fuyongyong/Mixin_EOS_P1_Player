# -*- coding:utf-8 -*-


from flask import (
    request,make_response)
from app.models import Father,Children
from app import app, db
import json
from functools import wraps

#===init plugins====
'''此处是插件'''
#==/init plugins====

#===cross_domain====
'''这个是允许跨域的代码'''

def allow_cross_domain(fun):

    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst

    return wrapper_fun
#==/cross_domain====

#===   pages    ===
'''此处是各个页面'''
@app.route('/page_name',methods=['POST'])
@allow_cross_domain
def the_function():
    id=msg_translate_from_front(request)['id'] #与前端交互
    example=msg_translate_from_front(request)['example']

    #=======获取信息=========

    #从数据库获取所有记录
    all_data=Father.query.all()

    #根据从前端获得的信息筛选出信息
    a_data=Father.query.filter_by(id=id,example=example).all()

    #筛选出第一个匹配项
    a_data=Father.query.filter_by(id=id,example=example).all()[0]

    #第一个匹配项中的某个属性
    an_attribute=Father.query.filter_by(id=id,example=example).all()[0].example

    #获取一列
    the_col=abstract_col(Father.query.all(),"id")
    #=======获取信息=========

    #=====修改数据库信息======

    #修改某条信息
    Father.query.filter_by(id=id).update({Father.id:id,\
                                                        Father.example:Father.example})
    db.session.commit()

    #新增某条信息

    #=====修改数据库信息======
    an_item=Father()
    an_item.id = id
    an_item.example="this_is an example"
    db.session.add(an_item)
    db.session.commit()

    # =====修改数据库信息======
    return msg_traslate_to_front(all_data)

#===   /pages   ===


#=== black code ===

'''Python格式=>前端数据'''
def msg_traslate_to_front(msg_all):
    try:
        msg_after_trans={msg_all[0].class_name:[]}

        for every_msg in msg_all:
            a_msg={}

            for every_vary in every_msg.class_varies:
                a_msg[every_vary]=every_msg.get_vary(every_vary)

            msg_after_trans[msg_all[0].class_name].append(a_msg)

        json_data=json.dumps(msg_after_trans)
        print("translate_to_front is {0}".format(json_data))
        #data format:{posts:[{a:b,c:d},{a:e,c:f}...]}
        return json_data
    except:
        return None

'''前端数据=>Python格式'''
def msg_translate_from_front(request):
    msg_data_old=request.form.to_dict()
    for i in msg_data_old:
        msg_data_new= json.loads(i)
    print("translate_from_front is {0}".format(msg_data_new))
    return msg_data_new

'''提取数据库中的列'''
def abstract_col(data, col_name):
    col = []
    for item in data:
        col.append(eval("item."+col_name))
    return col
#=== /black code ===

