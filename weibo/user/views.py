from flask import Blueprint, request, render_template, redirect, session
from libs.orm import db,check_login,check_psd,set_psd
from user.models import User
from hashlib import md5
import os

user_bp = Blueprint('user', __name__, url_prefix='/user')

user_bp.template_folder = './templates'


@user_bp.route('/home')
def home():
    return render_template('home.html')


@user_bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        city = request.form.get('city')
        tel = request.form.get('tel')

        filename = request.files.get('filename')
        if filename:
            file_bin=filename.stream.read()
            filename.stream.seek(0)
            file_md5=md5(file_bin).hexdigest()
            obj_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path=os.path.join(obj_dir,'static','img',file_md5)
            filename.save(file_path)
            filename = f'/static/img/{file_md5}'

        password=set_psd(password)
        try:
            new=User.query.filter_by(username=username).one()
            return f'{new.username}用户已存在'
        except Exception:

            user = User(username=username, password=password, gender=gender,
                        city=city, tel=tel ,filename=filename)
            db.session.add(user)
            db.session.commit()
            return redirect('/user/login')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter_by(username=username).one()
            uid=str(user.id)
            username = user.username
            if check_psd(password,user.password):
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
    uid = session['uid']
    user = User.query.get(uid)
    return render_template('user_info.html', user=user)


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
