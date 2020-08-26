from flask import Flask, redirect
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from libs.orm import db
from user.views import user_bp
from info.views import weibo_bp

app = Flask(__name__)
app.secret_key = r'jfi876&^^%89039jJ*7676382JhUUREJiw#$^^ow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:gao000@localhost:3306/weibo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 每次请求结束后都会自动提交数据库中的变动
db.init_app(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

app.register_blueprint(user_bp)
app.register_blueprint(weibo_bp)


@app.route('/')
def home():
    return redirect('/user/home')


if __name__ == '__main__':
    manager.run()
