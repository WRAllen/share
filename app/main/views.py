from . import main
from flask_login import login_required 
from flask import render_template, request,session
from app import db
from sqlalchemy import func,distinct,or_,desc
from app.auth.models import *
from flask import redirect, url_for
from app.auth.permissioncontrol import permissionControl

from datetime import datetime, timedelta

@main.route('/')
@login_required
def index():
	user_id = request.args.get("user_id")
	if user_id:
		page = request.args.get('page', 1, type=int)
		pagination = db.session.query(Thought.id, Thought.title, Thought.detail, Thought.label,Thought.zan, Thought.time).filter(Thought.user_id == user_id).paginate(page,per_page = 4) 
		thoughts = pagination.items
		return render_template('main/index.html',thoughts = thoughts, pagination = pagination)
	else:
		oldtime = (datetime.now()-timedelta(days=15)).strftime("%y-%m-%d")
		thoughts_15 = db.session.query( func.count(Thought.id).label('sum'), Thought.time ).filter( Thought.time > oldtime ).group_by( Thought.time ).all()
		array_15 = []
		for thought in thoughts_15:
			dic = {}
			dic["sum"] = thought[0]
			dic["time"] = thought[1].strftime("%Y-%m-%d")
			array_15.append(dic)

		labels = db.session.query( func.count(Thought.id).label('sum'),Thought.label ).filter(Thought.label != "").group_by(Thought.label).order_by(desc(func.count(Thought.id).label('sum'))).limit(3)
		array_3 = []
		
		for label in labels:
			dic = {}
			dic["value"] = label[0]
			dic["label"] = label[1]
			array_3.append(dic)

		thoughts = db.session.query(Thought.id, Thought.title, Thought.detail, Thought.label,Thought.zan, Thought.time).order_by(desc(Thought.zan)).limit(3)


		return render_template('data/showdata.html', array_15 = array_15, array_3 = array_3,thoughts = thoughts)

@main.route('/show')
@login_required
def show():
	key = request.args.get("key")
	name = '%' + key + '%'

	page = request.args.get('page', 1, type=int)
	pagination = db.session.query(Thought.id, Thought.title, Thought.detail, Thought.label,Thought.zan, Thought.time).filter(or_(Thought.detail.like(name), Thought.label.like(name), Thought.title.like(name))).paginate(page,per_page = 4) 
	thoughts = pagination.items


	return render_template('main/index.html',key = key, thoughts = thoughts, pagination = pagination)

@main.route('/search')
@login_required
def searchLabel():
	label = request.args.get("label")
	
	page = request.args.get('page', 1, type=int)
	pagination = db.session.query(Thought.id, Thought.title, Thought.detail, Thought.label,Thought.zan, Thought.time).filter(Thought.label == label).paginate(page,per_page = 4) 
	thoughts = pagination.items
	return render_template('main/index.html',key = label, thoughts = thoughts, pagination = pagination)


@main.route('/sharethought')
@login_required
def shareThought():
	user_id = request.args.get("user_id")
	detail = request.args.get("detail")
	label = request.args.get("label")
	title = request.args.get("title")

	time=datetime.now().strftime("%y-%m-%d")
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
	count = db.session.query(func.count( Thought.id), func.sum(Thought.zan)).filter(Thought.user_id == author.id).first()
	comments = Comment.query.filter_by(thought_id = thought.id).order_by('time').all()

	return render_template('main/showshare.html',thought = thought, author = author, comments = comments, sharenumber = count[0], zan = count[1])


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



@main.route('/zan')
@login_required
def zan():
	thought_id = request.args.get("thought.id")
	user_id = request.args.get("user.id")
	like = Like.query.filter_by(thought_id = thought_id , user_id =user_id).first()
	if like:
		return "false"
	else:
		like = Like(thought_id = thought_id , user_id =user_id)
		db.session.add(like)
		thought = Thought.query.filter_by(id = thought_id ).first()
		thought.zan+=1

		return "success"

@main.route('/changetitle')
@login_required
def changeTitle():
	thought_id = request.args.get("thought_id")
	thought_title = request.args.get("thought_title")

	thought = Thought.query.filter_by(id = thought_id).first()
	thought.title = thought_title
	time=datetime.now().strftime("%y-%m-%d %H:%M:%S")
	thought.time = time

	return "success"



@main.route('/changelabel')
@login_required
def changeLabel():
	thought_id = request.args.get("thought_id")
	thought_label = request.args.get("thought_label")
	thought_detail = request.args.get("thought_detail")

	thought = Thought.query.filter_by(id = thought_id).first()

	thought.label = thought_label
	thought.detail = thought_detail
	time=datetime.now().strftime("%y-%m-%d %H:%M:%S")
	thought.time = time

	return "success"

