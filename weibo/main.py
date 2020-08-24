from flask import Flask
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate

from libs.orm import db

app = Flask(__name__)
app.secret_key=r'jfi876&^^%89039jJ*7676382JhUUREJiwow'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://seamile:123@localhost:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 每次请求结束后都会自动提交数据库中的变动

manager=Manager(app)

migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)


@app.route('/')
def home():
    pass

if __name__ == '__main__':
    manager.run()