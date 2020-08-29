import random

from libs.orm import db, cn_str
from user.models import User, Follow


class Weibo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text, default='记下点生活的点滴')
    datetime = db.Column(db.DateTime)
    n_thumb = db.Column(db.Integer, nullable=False, default=0)

    @property
    def author(self):
        return User.query.get(self.uid)

    @property
    def colloct_users(self):
        clt_users = []
        for i in Colloct.query.filter_by(co_wid=self.id):
            clt_users.append(i.me_uid)
        return clt_users

    @property
    def follow_users(self):
        fo_users=[]
        for i in Follow.query.filter_by(other_uid=self.uid):
            fo_users.append(i.me_uid)
        return fo_users

    @classmethod
    def fake_weibos(cls, uid_li, num):
        wb_li = []
        for i in range(num):
            year = random.choice([2018, 2019, 2020])
            if year == 2020:
                mouth = random.randint(1, 8)
            else:
                mouth = random.randint(1, 12)
            day = random.randint(1, 28)
            date = '%04d-%02d-%02d' % (year, mouth, day)
            uid = random.choice(uid_li)
            content = cn_str(random.randint(50, 200))
            wb = cls(uid=uid, content=content, datetime=date)
            wb_li.append(wb)
        db.session.add_all(wb_li)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False, index=True)
    wid = db.Column(db.Integer, nullable=False, index=True)
    cid = db.Column(db.Integer, nullable=False, index=True, default=0)
    content = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    @property
    def author(self):
        '''获取当前评论的作者'''
        return User.query.get(self.uid)


class Thumb(db.Model):
    __tablename__ = 'thumb'

    other_uid = db.Column(db.Integer, primary_key=True, nullable=False)
    me_uid = db.Column(db.Integer, primary_key=True, nullable=False)


class Colloct(db.Model):
    __tablename__ = 'colloct'

    me_uid = db.Column(db.Integer, primary_key=True, nullable=False)
    co_wid = db.Column(db.Integer, primary_key=True, nullable=False)
    is_co = db.Column(db.Boolean, nullable=False, default=False)
