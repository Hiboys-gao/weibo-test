from flask import Blueprint,request,render_template,redirect
from libs.orm import db
from user.models import User
weibo_bp=Blueprint('weibo',__name__,url_prefix='/weibo',template_folder='./templates')
weibo_bp.static_folder='./static'