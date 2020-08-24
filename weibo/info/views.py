from datetime import datetime

from flask import Blueprint,request,render_template,redirect,session
from libs.orm import db
from info.models import Weibo
weibo_bp=Blueprint('weibo',__name__,url_prefix='/weibo',template_folder='./templates')
weibo_bp.static_folder='./static'


@weibo_bp.route('/home')
def home():
    infos=Weibo.query.order_by(Weibo.datetime.desc()).all()
    return render_template('home.html',infos=infos)

@weibo_bp.route('/weibo_info')
def weibo_info():
    uid = request.args.get('uid')
    info=Weibo.query.get(uid)
    session['uid']=uid
    return render_template('weibo_info.html',info=info)

@weibo_bp.route('/publish',methods=('POST','GET'))
def publish():
    if request.method=='POST':
        title=request.form.get('title')
        content=request.form.get('content')

        weibo=Weibo(title=title,content=content,datetime= datetime.now())
        db.session.add(weibo)
        db.session.commit()
        return redirect('/home')
    else:
        return render_template('publish.html')

@weibo_bp.route('/del')
def delete():
    uid=session['uid']
    Weibo.query.get(uid).delete()
    db.session.commit()
    return redirect('/weibo/home')

@weibo_bp.route('/modify',motheds=('POST','GET'))
def modify():
    uid = session['uid']
    if request.method=='post':
        title=request.form.get('title')
        content=request.form.get('content')
        Weibo.query.filter_by(id=uid).update({'title':title,'content':content,'datetime':datetime.now()})
        db.session.commit()
        return redirect('/weibo/home')
    else:
        return render_template('modify.html')