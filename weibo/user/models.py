from libs.orm import db, cn_str
import random, string


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True, index=True)
    password = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.Enum('男', '女', '保密'), nullable=False)
    city = db.Column(db.String(10))
    tel = db.Column(db.String(20))
    filename = db.Column(db.String(100))
    n_follow = db.Column(db.Integer, nullable=False, default=0)
    n_fans = db.Column(db.Integer, nullable=False, default=0)

    @classmethod
    def fake_users(cls, num):
        users = []
        for i in range(num):
            str_li = random.sample(string.ascii_lowercase, 3)
            num_li = random.sample(string.digits, 5)
            num_li.extend(random.sample(string.digits, 6))
            username = ''.join(str_li)
            password = '123456'
            gender = random.choice(['男', '女', '保密'])
            city = random.choice(['上海', '苏州', '长沙', '合肥', '呼和浩特', '青岛', '大理', '铁岭'])
            tel = ''.join(num_li)
            user = cls(username=username, password=password, gender=gender,
                       city=city, tel=tel)
            users.append(user)
        db.session.add_all(users)
        db.session.commit()
        return users


class Follow(db.Model):
    __tablename__ = 'follow'

    me_uid = db.Column(db.Integer, primary_key=True, nullable=False)
    other_uid = db.Column(db.Integer, primary_key=True, nullable=False)
