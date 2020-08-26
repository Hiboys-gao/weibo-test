from libs.orm import db



class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(16),nullable=False, unique=True,index=True)
    password = db.Column(db.String(200), nullable=False)
    gender=db.Column(db.Enum('男','女','保密'),nullable=False)
    city=db.Column(db.String(10))
    tel=db.Column(db.String(20))
    filename=db.Column(db.String(100))