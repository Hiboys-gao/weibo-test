from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect
import os, random
from hashlib import sha256
from functools import wraps


db = SQLAlchemy()


def set_psd(password):
    '''产生安全密码'''
    if not isinstance(password, bytes):
        password = password.encode('utf8')
    # 转换哈希值
    hash_wsd = sha256(password).hexdigest()
    # 产生随机盐
    salt = os.urandom(10).hex()
    # 加盐，产生安全密码
    safe_psd = salt + hash_wsd
    return safe_psd


def check_psd(psd1, safe_psd):
    if not isinstance(psd1, bytes):
        psd1 = psd1.encode('utf8')
    hash_psd = sha256(psd1).hexdigest()
    return hash_psd == safe_psd[20:]


def check_login(fun_view):
    @wraps(fun_view)
    def check_session(*args, **kwargs):
        uid = session.get('uid')
        if not uid:
            return redirect('/user/login')
        else:
            return fun_view(*args, **kwargs)
    return check_session


def cn_str(length):
    '''随机产生出一个中文字符串'''
    words = [chr(random.randint(19968, 25968)) for i in range(length)]
    return ''.join(words)



