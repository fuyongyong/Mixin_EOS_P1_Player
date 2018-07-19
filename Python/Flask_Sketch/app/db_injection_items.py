#-*- coding:utf-8 -*-
from app.models import *
from app import app,db

a_data=L2_Data()
a_data.id="1-1"
a_data.title="whatever"
a_data.abstract="whatever"
db.session.add(a_data)
db.session.commit()
'''
a_gv=Gv_Files()

a_gv.gv_title="first_one"
a_gv.gv_content="try it"
db.session.add(a_gv)
db.session.commit()

a_conception=Conceptions()

a_conception.conception_id="test1"
a_conception.conception_style="conception"
a_conception.conception_title="test"
a_conception.conception_content="测试一下"
a_conception.conception_gv_id=1
db.session.add(a_conception)
db.session.commit()

test1=db.session.query(Gv_Files.gv_id).all()
test2=Conceptions.query.filter_by(conception_gv_id=1).all()

def abstract_col(data,col_name):
    col=[]
    for item in data:
        col.append(item.col_name)
    return col
print(test2)

print(len(Gv_Files.query.all()))

a_r=Relationships()
a_r.id='index'
a_r.r_content=digraph G {
        "1"[label="1 你知道自己的未来是什么样子吗？\n未来基于个人和世界的复利"]
        "2"[label="2 你知道那条曲线究竟是什么吗？\n复利曲线"]
        "3" [label="3 究竟什么是财富自由？\n再也不用为了满足生活必须而出售自己的时间"]
        "4" [label="4 起步时最重要的是什么？\n用MAKE起步，然后「改进」"]
        "5" [label="5 你认真考虑过自己的商业模式吗？\n三种商业模式"]
        "6" [label="6 如何优化第一种个人商业模式？"]
        "7" [label="7 如何优化第二种个人商业模式？"]
        "8" [label="7 如何优化第三种个人商业模式？"]
	"1" ->"2"[label="未来基于个人和世界的复利"]
	"2" ->"3"[label="越过曲线，实现财富自由，首先要明确「概念」"]
	"3" ->"4"
	"3" ->"5"[label="出售时间的方式就是「个人商业模式」"]
	"5" ->"6"
	"5" ->"7"
	"5" ->"8"
}
db.session.add(a_r)
db.session.commit()
'''