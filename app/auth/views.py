# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash,make_response,session
from flask_login import login_user, logout_user, login_required 
from flask_login import current_user
from app.auth.models import *
from . import auth
from app.auth.permissioncontrol import permissionControl
from .forms import LoginForm,RegistrationForm
from .. import db
import json
from datetime import datetime
from emailTest import send_email
from sqlalchemy import or_
# 导入发送email的py文件



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)

            last_ip = request.remote_addr
            last_time = datetime.now().strftime("%y-%m-%d ")

            if user.ip_check(last_ip):
                user.last_time = last_time
                return make_response(redirect(request.args.get('next') or url_for('main.index')))
            else:
                return "异地登录!"
        flash("账户或者密码不正确!")

    return render_template('auth/login.html', form=form)


@auth.route('/logout') 
@login_required 
def logout():
    logout_user()

    flash('你已经退出登录！')

    return redirect(url_for('auth.login'))

###用户注册
@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() and form.validate():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)

        user.imgurl='/static/dist/img/user1.png'
        perms = db.session.query(Perm).filter(or_(Perm.id == 3, Perm.id == 2)).all()
        user.perms=perms

        ###给角色默认的头像
        db.session.add(user)
        ###这个很重要
        db.session.commit()


        token = user.generate_confirmation_token()

        send_email(user.email,'确认你的账户','auth/email/confirm',user,token)

        flash('账号验证已发送邮箱！')
        
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',form=form)




#需要带着token的账户进行登录一次才可以完成验证   
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    
    if current_user.confirmed:

        return redirect(url_for('main.index'))
        ##带修改
    if current_user.confirm(token):
        flash('你已经确认了你的账户，谢谢')

    else:
        flash('这个确认链接不可用，或已超时')

    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    '''
        如果返回响应或重定向，会直接发送至客户端，不会调用请求视图函数
    '''
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.'\
            and request.endpoint != 'static':

        return redirect(url_for('auth.unconfirmed'))

#尚未确认账户
@auth.route('/unconfirmed')
def unconfirmed():
    '''
        判断数据库的confirmed字段是否为True，如果为False(0),就跳转到提示确认账户界面
    '''
    if current_user.is_anonymous or current_user.confirmed:

        return redirect(url_for('main.index'))

    return render_template('auth/unconfirmed.html')



#重新发送账户确认邮件
@auth.route('/rendemail')
@login_required
def resend_confirmation():

    token = current_user.generate_confirmation_token()

    send_email(current_user.email, '确认你的账户',
               'auth/email/confirm', current_user, token)

    flash("已经重新发送一份邮件到你的邮箱")
    return redirect(url_for('auth.unconfirmed'))




@auth.route("/usermanage")
@permissionControl('auth.userManage')
@login_required 
def userManage():
    alluser=User.query.order_by(User.id).all()
    allrole=Role.query.order_by(Role.id).all()
    allperm=Perm.query.order_by(Perm.id).all()

    return render_template('auth/usermanage.html',alluser=alluser,allrole=allrole,allperm=allperm)



@auth.route("/urlmanage")
@permissionControl('auth.urlManage')
@login_required
def urlManage():
    '''
        管理路由和菜单
    '''
    allurl=Url.query.order_by(Url.id).all()
    allmenu=Menu.query.order_by(Menu.id).all()
    return render_template('auth/urlmanage.html',allurl=allurl,allmenu=allmenu)



@auth.route("/rolemanage")
@permissionControl('auth.roleManage')
@login_required 
def roleManage():
    '''
        管理角色和路由
    '''
    allurl = []

    allrole = Role.query.order_by(Role.id).all()
    allmenu = Menu.query.order_by(Menu.id).all()

    firstrole = Role.query.filter_by(id = 2).first()

    result2 = Url.query.order_by(Url.id).all()
    for x2 in result2:
        allurl.append([x2,x2.menus[0]])
        

    return render_template('auth/rolemanage.html',allrole=allrole,allurl=allurl,allmenu=allmenu,firstrole=firstrole)



@auth.route("/thoughtmanage")
@permissionControl('auth.thoughtManage')
@login_required 
def thoughtManage():
    '''
    用于管用户分享的想法
    '''
    allthought = db.session.query(Thought.id, Thought.title, Thought.label, Thought.detail, Thought.time, User.username, User.last_time).select_from(Thought, User).filter(Thought.user_id == User.id ).all()


    return render_template('auth/thoughtmanage.html',allthought = allthought )


@auth.route("/delthought")
@login_required
def delThought():
    thought_id = request.args.get("thought_id")

    allcomment = Comment.query.filter_by(thought_id = thought_id ).all()
    if allcomment:
        for x in allcomment:
            db.session.delete(x)

    alllike = Like.query.filter_by(thought_id = thought_id ).all()
    if alllike:
        for x2 in alllike:
            db.session.delete(x2)

    thought = Thought.query.filter_by(id = thought_id ).first()
    db.session.delete(thought)

    return "success"




@auth.route('/updaterolesource',methods=["POST"])
@login_required
def updateRoleSource():
    rolename=request.form.getlist('role_id')
    arr_urlid=request.form.getlist('now_url[]')
    str_split = rolename[0].split('_')[-1]
    roleid=int(str_split)
    role=Role.query.filter_by(id=roleid).first()
    role.urls=[]
    url = Url.query.filter(Url.id.in_(arr_urlid)).all()
    role.urls=url
    db.session.add(role)
    return "修改成功"



@auth.route('/updatesource')
@login_required
def update():
    '''
        ajax的访问地址,用于角色管理界面
    '''
    rolename=request.args.get('role_name')
    result=Role.query.filter_by(name=rolename).first()
    roleid=result.id
    role=Role.query.filter_by(id=roleid).first()
    dicta={}
    array=[]
    for x in role.urls:
        array.append(x.id)
    dicta['array']=array
    return json.dumps(dicta)



@auth.route('/updateuserinfo',methods=["POST"])
@login_required
def updateUserInfo():
    '''
        ajax的访问地址,用于修改信息
    '''
    userid=request.form.getlist('userid')
    arr_per=request.form.getlist('arr_per[]')
    activate=request.form.getlist('activate')
    rol_id=request.form.getlist('rol_id[]')
    user=User.query.filter_by(id=userid).first()
    ###查询出选择的用户
    perm=Perm.query.filter(Perm.id.in_(arr_per)).order_by(Perm.id).all()
    ###查询出选择的权限
    user.perms=perm
    confirmed=int(activate[0])
    ###把str转化为int
    user.confirmed=confirmed
    role=Role.query.filter(Role.id.in_(rol_id)).order_by(Role.id).all()
    user.roles=role
    db.session.add(user)

    return "success"



@auth.route('/updateurlmenu')
@login_required
def updateUrlMenu():
	'''
		ajax的访问地址,用于保存url与menu的关系
	'''
	now_url_menu = request.args.get('now_url_menu')
	now_url_name = request.args.get('now_url_name')
	url_id = request.args.get('url_id')
	url = Url.query.filter_by(id=url_id).first()
	menu = Menu.query.filter_by(name=now_url_menu).first()
	url.name = now_url_name
	url.menus = [menu]
	db.session.add(url)

	return "success"




@auth.route('/addrole')
@login_required
def addRole():
    role_name = request.args.get("role_name")
    role = Role.query.filter_by(name = role_name).first()
    if role:
        return "error"
    else:
        role = Role(name = role_name)
        db.session.add(role)
        return "success"

@auth.route('/updaterolename')
@login_required
def updateRoleName():
    new_role_name = request.args.get("new_role_name")
    old_role_name = request.args.get("old_role_name")
    role = Role.query.filter_by(name = old_role_name).first()
    if role:
        role.name = new_role_name
        return "success"
    else:
        return "error"


@auth.route("/deleterole")
@login_required
def deleteRole():
    role_name = request.args.get("role_name")
    role = Role.query.filter_by(name = role_name).first()
    if role:
        role.urls=[]
        users = User.query.all()
        for user in users:
            if role in user.roles:
                user.roles.remove(role)   
        db.session.commit()
        ###需要手动提交才可以，不然关联不会被删除        
        db.session.delete(role)
        return "success"
    else:
        return "error"
    
    


@auth.route('/addurl')
@login_required
def addURL():
    url_name = request.args.get("url_name")
    url_func = request.args.get("url_func")

    url = Url.query.filter_by(name = url_name).first()
    if url:
        return "error"
    else:
        url = Url(name = url_name,url_func = url_func)
        ini_menu = Menu.query.filter_by(name = '未分类').first()
        url.menus=[ini_menu]
        db.session.add(url)

        superadmin = Role.query.filter_by(id=1).first()
        superadmin.urls.append(url)
        return "success"


@auth.route("/deleteurl")
@login_required
def deleteURL():
    url_id = request.args.get("url_id")
    url = Url.query.filter_by(id = url_id).first()
    if url:
        url.menus=[]
        roles = Role.query.all()

        for role in roles:
            if url in role.urls:
                role.urls.remove(url)
                
        db.session.commit()
        ###需要手动提交才可以，不然关联不会被删除        
        db.session.delete(url)
        return "success"
    else:
        return "error"

@auth.route('/addmenu')
@login_required
def aaddMenu():
    menu_name = request.args.get("menu_name")
    menu = Menu.query.filter_by(name = menu_name).first()
    if menu:
        return "error"
    else:
        menu = Menu(name = menu_name)
        db.session.add(menu)
        return "success"


@auth.route('/updatemenu')
@login_required
def updateMenuName():
    new = request.args.get("new_menu_name")
    old = request.args.get("old_menu_name")

    menu = Menu.query.filter_by(name = old).first()
    if menu:
        menu.name = new
        return "success"
    else:
        return "error"


@auth.route("/deletemenu")
@login_required
def deleteMenu():
    menu_name = request.args.get("menu_name")
    menu = Menu.query.filter_by(name = menu_name).first()
    if menu:
        urls = Url.query.all()

        for url in urls:
            if menu in url.menus:
                url.menus.remove(menu)
                if len(url.menus)==0:
                    ini_menu = Menu.query.filter_by(name = '未分类').first()
                    url.menus=[ini_menu]
                
        db.session.commit()
        ###需要手动提交才可以，不然关联不会被删除        
        db.session.delete(menu)
        return "success"
    else:
        return "error"




