from sqlalchemy import MetaData, Table, Column, Integer, String
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

postgresql_db = engine()

post_meta = MetaData(bind=postgresql_db.engine)

post_meta.reflect(only=['customers'])

connection = postgresql_db.engine.connect()

columns_names = ['id', 'fname', 'lname', 'age']
columns_types = [Integer, String, String, Integer]
primary_key_flags = [True, False, False, False]
nullable_flags = [False, False, False, False]

test = Table('customers', post_meta,
             *(Column(column_name, column_type,
                      primary_key=primary_key_flag,
                      nullable=nullable_flag)
               for column_name,
                   column_type,
                   primary_key_flag,
                   nullable_flag in zip(columns_names,
                                        columns_types,
                                        primary_key_flags,
                                        nullable_flags)))

test.create()