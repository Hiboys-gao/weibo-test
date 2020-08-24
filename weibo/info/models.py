from libs.orm import db


class Weibo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),index=True,nullable=False)
    content=db.Column(db.Text,default='记下生活的点点滴滴')
    datetime=db.Column(db.DateTime)