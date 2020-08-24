from flask import Blueprint,request,render_template,redirect,session
from libs.orm import db
from user.models import User
user_bp=Blueprint('user',__name__,url_prefix='/user',template_folder='./templates')





@user_bp.route('/home')
def home():
    return render_template('home.html')

@user_bp.route('/register',methods=('POST','GET'))
def register():
    if request.method=='post':
        username=request.form.get('username')
        password=request.form.get('password')
        gender=request.form.get('gender')
        city=request.form.get('city')
        tel=request.form.get('tel')
        user= User(username=username,password=password,gender=gender,city=city,tel=tel)
        try:
            user_info=User.query.filter_by(username=username).one()
            if user_info:
                return '用户名已存在'
        except Exception:
            pass

        db.session.add(user)
        db.session.commit()
        return redirect('/user/login')
    else:
        return render_template('register.html')

@user_bp.route('/login',methods=('POST','GET'))
def login():
    if request.method=='post':
        username=request.form.get('username')
        password=request.form.get('password')
        try:
            user=User.query.filter_by(username=username).one()
            if user.password==password:
                session['uid']=user.id
                return redirect('/info/home')
            else:
                return '密码不正确'
        except Exception:
            return '用户名不存在'
    else:
        render_template('login.html')

@user_bp.route('/user_info')
def user_info():
    uid=session['uid']
    user=User.query.get(uid)
    return render_template('user_info.html',user=user)

@user_bp.route('/logout')
def logout():
    session.pop('uid')
    redirect('user/home')