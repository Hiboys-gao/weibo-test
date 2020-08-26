from datetime import datetime
import random,math

from flask import Blueprint, request, render_template, redirect, session
from libs.orm import db,check_login
from info.models import Weibo

weibo_bp = Blueprint('weibo', __name__, url_prefix='/weibo')
weibo_bp.template_folder = './templates'
weibo_bp.static_folder = './static'


@weibo_bp.route('/home')
def home():
    try:
        infos = Weibo.query.order_by(Weibo.datetime.desc())
        count=Weibo.query.count()
        count_li=[]
        page=math.ceil(count / 20)

        if count <= 20:
            return render_template('weibo_home.html', infos=infos.all() ,count_li=count_li)
        else:
            for z in range(page):
                count_li.append(z)
            print(count_li)
            page_con=request.args.get('page')

            if page_con:
                page_con=int(page_con)
                print(page_con)
                if page_con > 1:
                    return render_template('weibo_home.html', infos=infos.limit(20).offset(20*(page_con-1)).all(), count_li=count_li)
                else:

                    return render_template('weibo_home.html', infos=infos.limit(20).all(), count_li=count_li, )
            else:

                return render_template('weibo_home.html', infos=infos.limit(20).all(), count_li=count_li,)

    except Exception:
        return redirect('/weibo/publish')


@weibo_bp.route('/weibo_info')
def weibo_info():
    wb_id = request.args.get('wb_id')
    info = Weibo.query.get(wb_id)
    return render_template('weibo_info.html', info=info)


@weibo_bp.route('/publish', methods=('POST', 'GET'))
@check_login
def publish():
    '''
    for i in range(1,30):
        li=[x for x in range(19968,21968)]
        title_nums= random.sample(li,6)
        title=''
        for y in title_nums:
            title += chr(y)
        content_nums = random.sample(li, 100)
        content = ''
        for z in content_nums:
            content += chr(z)
        weibo = Weibo(title=title, content=content, datetime=datetime.now())
        db.session.add(weibo)
        db.session.commit()
    '''

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        weibo = Weibo(title=title, content=content, datetime=datetime.now())
        db.session.add(weibo)
        db.session.commit()
        return redirect('/weibo/home')
    else:
        return render_template('publish.html')


@weibo_bp.route('/delete')
@check_login
def delete():
    wb_id = int(request.args.get('wb_id'))
    Weibo.query.filter_by(id=wb_id).delete()
    db.session.commit()
    return redirect('/weibo/home')


@weibo_bp.route('/modify', methods=('POST', 'GET'))
@check_login
def modify():
    wb_id = request.args.get('wb_id')
    weibo = Weibo.query.filter_by(id=wb_id).one()
    if request.method == 'post':
        title = request.form.get('title')
        content = request.form.get('content')
        weibo.update({'title': title, 'content': content, 'datetime': datetime.now()})
        db.session.commit()
        return redirect('/weibo/home')
    else:
        return render_template('modify.html', weibo=weibo)
