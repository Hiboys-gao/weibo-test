from flask import Blueprint, request, render_template, redirect, session
from sqlalchemy.exc import IntegrityError

from libs.orm import db, check_login, check_psd, set_psd
from libs.def_orm import Mr_big
from user.models import User,Follow
from info.models import Weibo
from hashlib import md5
import os

user_bp = Blueprint('user', __name__, url_prefix='/user')

user_bp.template_folder = './templates'


@user_bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password')
        print(password)
        gender = request.form.get('gender')
        city = request.form.get('city', '').strip()
        tel = request.form.get('tel', '').strip()

        filename = request.files.get('filename')
        if filename:
            file_bin = filename.stream.read()
            filename.stream.seek(0)
            file_md5 = md5(file_bin).hexdigest()
            obj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(obj_dir, 'static', 'img', file_md5)
            filename.save(file_path)
            filename = f'/static/img/{file_md5}'

        password = set_psd(password)
        print(password)
        try:
            new = User.query.filter_by(username=username).one()
            return f'{new.username}用户已存在'
        except Exception:

            user = User(username=username, password=password, gender=gender,
                        city=city, tel=tel, filename=filename)
            db.session.add(user)
            db.session.commit()
            return redirect('/user/login')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            user = User.query.filter_by(username=username).one()
            uid = user.id
            username = user.username
            if check_psd(password, user.password):
                session['uid'] = uid
                session['username'] = username
                return redirect('/weibo/home')
            else:
                return '密码不正确'
        except Exception:
            return '用户名不存在'
    else:
        return render_template('login.html')


@user_bp.route('/user_info')
@check_login
def user_info():
    w_uid=int(request.args.get('w_uid',0))
    uid = session['uid']
    if w_uid:
        user = User.query.get(w_uid)
    else:
        user = User.query.get(uid)
    weibos = Weibo.query.filter_by(uid=uid).order_by(Weibo.datetime.desc())
    wb_li = [wb for wb in weibos]
    return render_template('user_info.html', user=user, wb_li=wb_li)


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user_bp.route('/follow')
@check_login
def follow():
    uid=session['uid']
    wb_id=int(request.args.get('wb_id'))
    other_uid=Weibo.query.get(wb_id).uid
    path= f"{request.args.get('path')}?wb_id={wb_id}"
    follow=Follow(me_uid=uid,other_uid=other_uid)
    try:
        User.query.filter_by(id=uid).update({'n_follow':User.n_follow + 1})
        User.query.filter_by(id=other_uid).update({'n_fans':User.n_fans + 1})
        db.session.add(follow)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        Follow.query.filter_by(me_uid=uid,other_uid=other_uid).delete()
        User.query.filter_by(id=uid).update({'n_follow': User.n_follow - 1})
        User.query.filter_by(id=other_uid).update({'n_fans': User.n_fans - 1})
        db.session.commit()
    return redirect(path)


@user_bp.route('/follow_fans')
@check_login
def follow_user():
    uid=session['uid']
    fo_users_li=[]
    try:
        fo_users=Follow.query.filter_by(me_uid=uid)
        for user in fo_users:
            fo_weibo=Weibo.query.filter_by(uid=user.other_uid).order_by(Weibo.datetime.desc()).limit(2)
            fo_user=User.query.filter_by(id=user.other_uid).one()
            fo_users_li.append({'user':fo_user,'weibo':fo_weibo})
        return render_template('follow_fans.html',fo_users_li=fo_users_li,bigs=Mr_big())
    except IntegrityError:
        return redirect('/weibo/home')


@user_bp.route('/fans_follow')
@check_login
def fans_user():
    uid = session['uid']
    fo_users_li = []
    try:
        fo_users = Follow.query.filter_by(other_uid=uid)
        for user in fo_users:
            fo_weibo = Weibo.query.filter_by(uid=user.me_uid).order_by(Weibo.datetime.desc()).limit(2)
            fo_user = User.query.filter_by(id=user.me_uid).one()
            fo_users_li.append({'user': fo_user, 'weibo': fo_weibo})
        return render_template('follow_fans.html', fo_users_li=fo_users_li,bigs=Mr_big())
    except IntegrityError:
        return redirect('/weibo/home')