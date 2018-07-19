# -*- coding:utf-8 -*-


from flask import (
    request,make_response)
from app import app
import json
from functools import wraps


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
#===    end     ===

#======index.html=======
'''这里是index中用到的API接口'''

'''indx_svg_list：获取gv列表'''
@app.route('/index_get_command',methods=['POST'])
@allow_cross_domain

def index_get_command():
    ter_command=msg_translate_from_front(request)['tercommand']
    if ter_command=="test":
        return "test.html"
    else:
        return "Wrong"


#===    end     ===

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
        print(json.dumps(msg_after_trans))
        #data format:{posts:[{a:b,c:d},{a:e,c:f}...]}
        return json.dumps(msg_after_trans)
    except:
        return None

'''前端数据=>Python格式'''
def msg_translate_from_front(request):
    msg_data_old=request.form.to_dict()
    for i in msg_data_old:
        msg_data_new= json.loads(i)
    print(msg_data_new)
    return msg_data_new

#===    end     ===
