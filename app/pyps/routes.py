from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, Category, Subcategory, Info, Hardware, \
Script, Journal
from app.main.forms import  NetworkForm, DeleteForm,RemoveForm
from app.pyps.forms import PypScriptsForm
from requests import Request, Session
from app.pyps import bp
from flask_login import login_required, current_user
from flask_babel import _, get_locale
import os
import requests
from app import db
from app.edit.routes import delete

@bp.route('/pyps_index',methods=['GET', 'POST'])
@login_required
def index():
    
    form=PypScriptsForm()

    if form.validate_on_submit():
    	u=Script(name=form.name.data)
    	db.session.add(u)
    	db.session.commit()
    	script_name='Script_'+form.name.data+'.txt'
    	folder=os.environ.get('SCRIPT_FOLDER')
    	file= open(folder+script_name,'w')
    	file.write(form.body.data)
    return render_template('pyps/index.html',form=form)










