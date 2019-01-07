from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from time import time
import jwt
from flask import current_app
from app.search import add_to_index, remove_from_index, query_index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)










 
#Association table, auxilary table , has no data in it, just the foreign keys for the user entries many to many relationship

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

basket= db.Table('basket',
    db.Column('info_id', db.Integer, db.ForeignKey('info.id')),
    db.Column('location_id', db.Integer, db.ForeignKey('location.id'))

   
)



class User(UserMixin,db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    posts_r = db.relationship('Post_r', backref='author_r', lazy='dynamic')
    statistics = db.relationship('Statistic', backref='user_s', lazy='dynamic')
    journals = db.relationship('Journal', backref='user_j', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    @login.user_loader
    #db relationship between left sider User(Parent Class) and right side user defined under ('User,...
    #secondary configures the association table I defined above the class
    #primaryjoin indicates thecondition that links the left side entity(the follower user) with the association table
    #secondaryjoin indicates the condition that links the right side user/the followed user) with the association table
    #backref defines how the the relationship will be acced from the right side user
        

    def load_user(id):
        return User.query.get(int(id))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User {}>'.format(self.username)

#Password reset token fields 

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

#functions to  follow unfollow user 

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
#query all entries user followed



    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

#Create Avatar Icon for User

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)    


class Post(db.Model, SearchableMixin): # ,SearchableMixin needs to be added
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))
    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Info(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    infotext=db.Column(db.String(140))
    



class Customer(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(140) ,index=True, unique=True)
    locations =db.relationship('Location', backref='customer')


class Network(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(140))
    network=db.Column(db.String(140))
    fromip = db.Column(db.String(140))
    toip = db.Column(db.String(140))
    gateway= db.Column(db.String(140))
    subnet= db.Column(db.String(140))
    cdir = db.Column(db.String(140))
    vip = db.Column(db.String(140))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    

class Location(db.Model, SearchableMixin):
    __searchable__ = ['contract']

    customer_id=db.Column(db.Integer, db.ForeignKey('customer.id'))
    id = db.Column(db.Integer, primary_key=True)
    residence = db.Column(db.String(140))
    technology = db.Column(db.String(140))
    project= db.Column(db.String(140))
    projectmanager=db.Column(db.String(140))
    hardware= db.relationship('Hardware', backref='location' , lazy='dynamic')
    networks= db.relationship('Network', backref='location' , lazy='dynamic')
    journals= db.relationship('Journal', backref='location' , lazy='dynamic')
    contract= db.Column(db.String(140))
    contact=db.Column(db.String(140))
    sid= db.Column(db.String(140))
    matchcode= db.Column(db.String(140))
    seller= db.Column(db.String(140))
    vrf= db.Column(db.String(140))
    dependencies=db.relationship('Contract', backref='location' , lazy='dynamic')
    infos=db.relationship("Info", secondary="basket", backref='locations')
    connector=db.Column(db.String(280))

    def __repr__(self):
        return '<Location {}>'.format(self.residence)


    def remove_info(self,info):
        self.infos.remove(info)

class Hardware(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(140))
    sn = db.Column(db.String(140))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(140))
    contract=db.Column(db.String(140))
    location_idc = db.Column(db.Integer, db.ForeignKey('location.id'))

    



class Post_r(db.Model): # ,SearchableMixin needs to be added
    
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    
    def __repr__(self):
        return '<Post_r {}>'.format(self.body)





class Statistic(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    technology=db.Column(db.String(140))
    time=db.Column(db.String(140))
    customer=db.Column(db.String(140))
    contract=db.Column(db.String(140))
    hardware=db.Column(db.String(140))
    user=db.Column(db.String(140))
    user_id_stat=db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'))
    subcategory_id=db.Column(db.Integer, db.ForeignKey('subcategory.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    




class Category(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(140))
    statistics= db.relationship('Statistic', backref='category')




class Subcategory(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(140))
    statistics= db.relationship('Statistic', backref='subcategory')


def dynamic_class(table_name, columns):
    dyn_table=type(table_name, (Base,), columns)

    return dyn_table

class test(db.Model):
    id=db.Column(db.Integer, primary_key=True)


class Script(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(140) ,index=True, unique=True)

class Journal(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(140) ,index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id_journal=db.Column(db.Integer, db.ForeignKey('user.id'))
    location_id_journal=db.Column(db.Integer, db.ForeignKey('location.id'))
    link=db.Column(db.String(140) ,index=True)

class Template(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(380) ,index=True)



    




