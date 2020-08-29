from user.models import User
from info.models import Weibo


def Mr_big():
    return User.query.order_by(User.n_fans.desc()).limit(10)


def hot_weibo():
    return Weibo.query.order_by(Weibo.n_thumb.desc()).limit(10)
