from datetime import datetime
import random, math

from flask import Blueprint, request, render_template, redirect, session
from sqlalchemy.exc import IntegrityError

from libs.orm import db, check_login
from libs.def_orm import hot_weibo
from info.models import Weibo, Comment, Thumb, Colloct

weibo_bp = Blueprint('weibo', __name__, url_prefix='/weibo')
weibo_bp.template_folder = './templates'
weibo_bp.static_folder = './static'


@weibo_bp.route('/home')
def home():
    try:
        wid = int(request.args.get('wb_id', 0))
        weibos = Weibo.query.order_by(Weibo.datetime.desc())
        per_page = 15
        if wid:
            wid_time = weibos.filter_by(id=wid).one().datetime
            page = math.ceil(Weibo.query.filter(Weibo.datetime >= wid_time).count() / per_page)
        else:
            page = int(request.args.get('page', 1))
        offset = per_page * (page - 1)
        wb_li = Weibo.query.order_by(Weibo.datetime.desc()).limit(per_page).offset(offset)
        max_page = math.ceil(Weibo.query.count() / 15)
        print(max_page)
        if page <= 3:
            start, end = 1, 6
        elif page > (max_page - 3):
            start, end = max_page - 3, max_page
        else:
            start, end = (page - 3), (page + 3)
        pages = range(start, end + 1)
        print(pages)
        return render_template('weibo_home.html', wb_li=wb_li, pages=pages, max_page=max_page,
                               weibos=hot_weibo())
    except Exception:
        return redirect('/weibo/publish')


@weibo_bp.route('/weibo_info')
def weibo_info():
    wb_id = int(request.args.get('wb_id'))
    info = Weibo.query.get(wb_id)
    cn_li = []
    try:
        co_infos = Comment.query.filter_by(wid=wb_id)
        comments = co_infos.filter_by(cid=0).order_by(Comment.datetime.desc())
        for comment in comments:
            cn_dic = {'comment': comment, 'replys': None}
            try:
                replys = co_infos.filter_by(cid=comment.id).order_by('datetime')
                cn_dic['replys'] = replys
            except Exception:
                print('没有回复')
            cn_li.append(cn_dic)
    except Exception:
        print('没有评论')
    return render_template('weibo_info.html', info=info, cn_li=cn_li, weibos=hot_weibo())


@weibo_bp.route('/publish', methods=('POST', 'GET'))
@check_login
def publish():
    # 导入 一些微博
    # for i in range(1, 30):
    #     li_cn = [x for x in range(19968, 21968)]
    #     li_point=[x for x in range(33, 48)]
    #     cn_li=[]
    #     point_li=[]
    #     for j in range(100):
    #         cn_li.append(chr(random.choice(li_cn)))
    #     for k in range(3):
    #         point_li.append(chr(random.choice(li_point)))
    #     cn_li.extend(point_li)
    #     content_li=list(set(cn_li))
    #     content = ''.join(content_li)+'。'
    #
    #     year = random.choice([2019, 2020])
    #     if year == 2020:
    #         mouth = random.randint(1, 8)
    #     else:
    #         mouth = random.randint(1, 12)
    #     day = random.randint(1, 28)
    #     hour=random.randint(1, 24)
    #     min=random.randint(1, 59)
    #     sec=random.randint(1, 59)
    #     date = '%04d-%02d-%02d %02d:%02d:%02d' % (year, mouth, day,hour,min,sec)
    #
    #     weibo = Weibo(uid=47, content=content, datetime=date)
    #     db.session.add(weibo)
    #     db.session.commit()

    if request.method == 'POST':
        uid = session['uid']
        content = request.form.get('content')
        weibo = Weibo(uid=uid, content=content, datetime=datetime.now())
        db.session.add(weibo)
        db.session.commit()
        return redirect(f'/weibo/weibo_info?wb_id={weibo.id}')
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
    if request.method == 'post':
        content = request.form.get('content')
        wb_id = int(request.form.get('wb_id'))
        print(wb_id)
        weibo = Weibo.query.get(wb_id)
        weibo.content = content
        weibo.datetime = datetime
        db.session.commit()
        return redirect('/weibo/home')
    else:
        wb_id = request.args.get('wb_id')
        weibo = Weibo.query.get(wb_id)
        return render_template('modify.html', weibo=weibo)


@weibo_bp.route('/comment', methods=('POST', 'GET'))
def comment():
    uid = session.get('uid')
    if uid:
        info = request.form.get('content')
        if info:
            wid = request.form.get('wid')
            comment = Comment(content=info, wid=wid, uid=uid, datetime=datetime.now())
            db.session.add(comment)
            db.session.commit()
            return redirect(f'/weibo/weibo_info?wb_id={wid}')
        else:
            return '评论内容不能没空！！！'
    else:
        return redirect('/user/login')


@weibo_bp.route('/reply', methods=('POST', 'GET'))
def reply():
    uid = session.get('uid')
    if uid:
        content = request.form.get('content')
        if content:
            wid = request.form.get('wid')
            cid = request.form.get('cid')
            dt = datetime.now()
            comment = Comment(content=content, wid=wid, uid=uid, cid=cid, datetime=dt)
            db.session.add(comment)
            db.session.commit()
            return redirect(f'/weibo/weibo_info?wb_id={wid}')
        else:
            return '回复内容不能没空！！！'
    else:
        return redirect('/user/login')


@weibo_bp.route('/del_comment')
@check_login
def del_comment():
    cmt_id = int(request.args.get('id'))
    wid = int(request.args.get('wid'))
    Comment.query.filter_by(id=cmt_id).delete()
    db.session.commit()
    return redirect(f'/weibo/weibo_info?wb_id={wid}')


@weibo_bp.route('/thumb')
@check_login
def thumb():
    me_uid = session['uid']
    wid = int(request.args.get('wid'))
    thumb = Thumb(me_uid=me_uid, other_uid=wid)
    path = f"{request.args.get('path')}?wb_id={wid}"
    try:
        Weibo.query.filter_by(id=wid).update({'n_thumb': Weibo.n_thumb + 1})
        db.session.add(thumb)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        Weibo.query.filter_by(id=wid).update({'n_thumb': Weibo.n_thumb - 1})
        Thumb.query.filter_by(me_uid=me_uid, other_uid=wid).delete()
        db.session.commit()
    return redirect(path)


@weibo_bp.route('/collect')
@check_login
def collect():
    me_uid = session['uid']
    wb_id = int(request.args.get('wb_id'))
    clt = Colloct(me_uid=me_uid, co_wid=wb_id, is_co=True)
    path = f"{request.args.get('path')}?wb_id={wb_id}"
    try:
        db.session.add(clt)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        Colloct.query.filter_by(me_uid=me_uid, co_wid=wb_id).delete()
        db.session.commit()
    return redirect(path)
