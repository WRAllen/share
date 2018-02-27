# -*- coding:utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,current_user
from .. import db, login_manager
from app.models import BaseTable,tab_relation
from flask import current_app



user_role = tab_relation('user_role', 'user_id', 'user.id', 'role_id', 'role.id')
user_perm = tab_relation('user_perm', 'user_id', 'user.id', 'perm_id', 'perm.id')
role_url = tab_relation('role_url', 'role_id', 'role.id', 'url_id', 'url.id')
url_menu = tab_relation('url_menu', 'url_id', 'url.id', 'menu_id', 'menu.id')


class Perm(BaseTable):
    users=db.relationship(
        'User',
        secondary=user_perm,
        backref=db.backref('perm',lazy='dynamic')
    )


class Menu(BaseTable):
    urls=db.relationship(
        'Url',
        secondary=url_menu,
        backref=db.backref('menu',lazy='dynamic')
    )


class Role(BaseTable):
    users=db.relationship(
        'User',
        secondary=user_role,
        backref=db.backref('role',lazy='dynamic')
    )
    urls=db.relationship(
        'Url',
        secondary=role_url,
        backref=db.backref('role',lazy='dynamic')
    )



class Url(BaseTable):
    url_func = db.Column(db.String(64))
    roles=db.relationship(
        'Role',
        secondary=role_url,
        backref=db.backref('url',lazy='dynamic')
    )
    menus=db.relationship(
        'Menu',
        secondary=url_menu,
        backref=db.backref('url',lazy='dynamic')
    )

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    label = db.Column(db.String(20))
    style = db.Column(db.Integer)
    time = db.Column(db.Date)
    zan = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(64),nullable = False)
    detail = db.Column(db.Text)
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    thought_id = db.Column(db.Integer,db.ForeignKey('thought.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
 
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    thought_id = db.Column(db.Integer, db.ForeignKey('thought.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('thought.user_id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer = db.Column(db.Text)
    time = db.Column(db.DateTime)

class User(UserMixin, BaseTable):
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True, index=True)
    name = db.Column(db.String(64))
    ###重写name,user的昵称可重复
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean,default=False)
    tel = db.Column(db.String(13))
    ip = db.Column(db.String(15))
    entry = db.Column(db.Boolean,default=True)
    last_time = db.Column(db.DateTime)
    sex = db.Column(db.Boolean)
    birthday = db.Column(db.Date)
    imgurl = db.Column(db.String(128))

    thoughts = db.relationship("Thought")

    roles=db.relationship(
        'Role',
        secondary=user_role,
        backref=db.backref('user',lazy='dynamic')
    )
    perms=db.relationship(
        'Perm',
        secondary=user_perm,
        backref=db.backref('user',lazy='dynamic')
    )


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def user_can(self):
        array_role_url=[]
        url_ids=[]
        allrole=current_user.roles
        for role in allrole:
            allurl=role.urls
            for url in allurl:
                url_ids.append(url.id)
        url_ids=list(set(url_ids))
        allurl=Url.query.filter(Url.id.in_(url_ids)).all()
        return allurl

    def is_superadmin(self):
        if current_user.username== 'admin':
            return True
        else:
            return False

    def ip_check(self,last_ip):
        if current_user.ip != None:
            array = []
            for x in range(0,4):
                new = last_ip.split('.')[x]
                old = current_user.ip.split('.')[x]
                if new == old :
                    array.append(x)  

            if 0 in array and 1 in array and 2 in array:
                current_user.ip = last_ip
                return True
            else:
                return False
        else:
            current_user.ip = last_ip
            return True



@login_manager.user_loader
def load_user(user_uid):
    return User.query.get(int(user_uid))

