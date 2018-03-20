# -*- coding:utf-8 -*-
from flask import Flask,render_template
from flask_mail import Mail, Message
app = Flask(__name__)
'''
	    1 邮箱服务
        2 邮箱端口
        3 发送邮箱
        4 邮箱授权码
	'''
app.config.update(
	MAIL_SERVER='smtp.qq.com',
	MAIL_PORT='465',
	MAIL_USE_SSL=True,
	MAIL_USERNAME='1072274105',
	MAIL_PASSWORD='cqigcudcganjbdgi'
	)
mail = Mail(app)

def send_email(to,subject,template,user,token):
	'''
		1 实例化Message对象
		2 设置发送邮件的内容
		3 发送邮件
	'''
	msg = Message(subject, sender='1072274105@qq.com', recipients=[to])
	msg.html = render_template(template + '.txt', user=user,token=token)
	mail.send(msg)
