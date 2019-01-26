from app.main.forms import EditProfileForm, PostForm, LocationForm, NetworkForm,JournalForm, \
CustomerForm, Post_r_Form, StatisticForm, DeleteForm, InfoForm,RemoveForm,ScriptForm, \
TemplateForm,GetNetworksForm, RouterForm,RouterbyTimeForm
from app.models import User, Post, Location, Customer, Network, Post_r, \
Statistic, Category, Subcategory, Info, Hardware,Script,Template,Journal
import inspect
from app import db
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, PostForm, LocationForm, NetworkForm,JournalForm, \
CustomerForm, Post_r_Form, StatisticForm, DeleteForm, InfoForm,RemoveForm,ScriptForm, \
TemplateForm,GetNetworksForm, RouterForm,RouterbyTimeForm
from app.models import User, Post, Location, Customer, Network, Post_r, \
Statistic, Category, Subcategory, Info, Hardware,Script,Template,Journal
from guess_language import guess_language
from werkzeug.utils import secure_filename
import os
from app.pandaex import  sendpandas
from app.main.forms import SearchForm
from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import bs4 as bs
import pandas as pd
from app.file.routes import expynew
from app.edit.routes import delete
from app.functions.sshcon import if_connector
from flask import session
from requests import get
from flask import Response
from flask import stream_with_context
import urllib.parse
import flask
import logging
from app.functions.router_config import create_config
from app.functions.get_data import bo_ilvt
from collections import OrderedDict
from app.main.list_variables import entries
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, HiddenField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, AnyOf, InputRequired
import time

from datetime import datetime
import inspect
import wtforms
from sqlalchemy.inspection import inspect



def add_cols(main_db, form_instance,*sub_dbs):
    strings_in_db=[]
    foreignkeys_in_db=[]
    list_buttons=['save','submit','send','delete']
    db_name=main_db.__name__
   
               
        

    table = inspect(main_db)
        
    for column in table.c:
            
        if 'VARCHAR' in str(column.type):
            strings_in_db.append(column.name)
        if '_id' in str(column.name):
            foreignkeys_in_db.append(column.name.split('_')[0])

    class_data=form_instance.__dict__
    dict_class={}
    for i in class_data:
            
        if '_' not in i:
                
            data=getattr(form_instance, i)
                
            try:
                dict_class[i]=data.data


            except:
                print('wrong type')

       
    dblist=sub_dbs

    foreignkeys_in_db.extend(list_buttons)

    

    for i in foreignkeys_in_db:
        print(i)
        
      
    entries_to_remove(foreignkeys_in_db, dict_class)

       

        

       




       # for i in dict_class:
        #    if isinstance(dict_class.get(i), int):
         #       print('Integer found' + str(i))

        



        
            
        
    obj_data=main_db(**dict_class)

    db.session.add(obj_data)
    db.session.commit()
    dict_db={}
    db_name_string=str(db_name).lower()+'s'
       

        

        

        

            
          

        

    for i in dblist:
        if i == User:
            user=User.query.filter_by(username=current_user.username).first()
            getattr(user, db_name_string).append(obj_data)

        y=getattr(i, 'query').get(form_instance.category.data)
        getattr(y, db_name_string).append(obj_data)

       
    db.session.commit()
    














    return 'works'



def entries_to_remove(entries, dict_data):
    for key in entries:
        if key in dict_data:
            del dict_data[key]



            
                


