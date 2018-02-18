from . import main
from flask_login import login_required 
from flask import render_template, request,session
from app import db
from sqlalchemy.sql import func,distinct,or_
from app.auth.models import *
from flask import redirect, url_for
from app.auth.permissioncontrol import permissionControl

from datetime import datetime

@main.route('/')
@login_required
def index():
	return render_template('main/index.html')

@main.route('/show')
@login_required
def show():
	key = request.args.get("key")
	name = '%' + key + '%'

	page = request.args.get('page', 1, type=int)
	pagination = db.session.query(Thought.id, Thought.title, Thought.detail,Thought.label).filter(or_(Thought.detail.like(name), Thought.label.like(name), Thought.title.like(name))).paginate(page,per_page = 4) 
	thoughts = pagination.items


	return render_template('main/index.html',key = key, thoughts = thoughts, pagination = pagination)


@main.route('/sharethought')
@login_required
def shareThought():
	user_id = request.args.get("user_id")
	detail = request.args.get("detail")
	label = request.args.get("label")
	title = request.args.get("title")

	time=datetime.now().strftime("%y-%m-%d %H:%M:%S")
	if detail == None:
		detail = Null
	if label == None:
		label = Null
	
	thought = Thought(label = label, style = 0, user_id = user_id, time = time, detail =  detail, title = title )
	db.session.add(thought)

	return "success"


@main.route('/share/<ThoughtId>')
@login_required
def showThought(ThoughtId):
	thought = Thought.query.filter_by(id=ThoughtId).first()
	author = User.query.filter_by(id=thought.user_id).first()
	sharenumber = db.session.query(func.count( Thought.id) ).filter(Thought.user_id == author.id).first()
	comments = Comment.query.filter_by(thought_id = thought.id).order_by('time').all()


	return render_template('main/showshare.html',thought = thought, author = author, comments = comments, sharenumber = sharenumber[0])


@main.route('/commit')
@login_required
def commit():
	answer = request.args.get("answer")
	answer_id = request.args.get("answer_id")
	thought_id = request.args.get("thought_id")
	author_id = request.args.get("author_id")
	time=datetime.now().strftime("%y-%m-%d %H:%M:%S")

	comment = Comment(answer = answer, answer_id = answer_id, thought_id = thought_id, author_id = author_id, time = time)
	db.session.add(comment)

	return "success"


@main.route('/showhead')
@login_required
def showHead():
	answer_id = request.args.get("answer_id")
	user = User.query.filter_by(id = answer_id).first()
	return user.imgurl



