# -*- coding:utf-8  -*-

from app import db

class Father(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    example=db.Column(db.String(25))
    children = db.relationship('Children', backref='father', lazy='dynamic')

    class_name="Father"
    class_varies=['id','example']
    def get_vary(self, vary_name):
        return eval("self." + vary_name)

class Children(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    father_id = db.Column(db.String(25), db.ForeignKey('father.id'))
    class_name="Children"
    example=db.Column(db.String(25))
    class_varies=['id','father_id']
    def get_vary(self, vary_name):
        return eval("self." + vary_name)






