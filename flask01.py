from app import create_app, db, cli
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, Category, Subcategory,Contract, Info, basket,Script,Template
import os


app=create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post,'Location': Location, 'Customer': Customer, 'Network': Network, 'Post_r' : Post_r,
    'Statistic': Statistic, 'Category': Category, 'Subcategory': Subcategory, 'Contract': Contract, 'Info': Info,'basket': basket,'Script':Script,'Template': Template}

pathv='mysql+pymysql://flask01:Katze7436!@localhost:3306/flask01'
os.environ['DATABASE_URL']=pathv

