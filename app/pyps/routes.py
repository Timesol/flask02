from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, Category, Subcategory, Info, Hardware, \
Script, Journal,Template
from app.main.forms import  NetworkForm, DeleteForm,RemoveForm
from app.pyps.forms import PypScriptsForm, CreateTemplateForm
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
    form_template=CreateTemplateForm()

    if form.validate_on_submit():
        if form.submit.data:
            print('wrong if')
            u=Script(name=form.name.data)
            db.session.add(u)
            db.session.commit()
            script_name='Script_'+form.name.data+'.txt'
            folder=os.environ.get('SCRIPT_FOLDER')
            file= open(folder+script_name,'w')
            file.write(form.body.data)
            return redirect(url_for('pyps.index'))

    


    if form_template.validate_on_submit():
        if form_template.create.data:
            print('Correct if')
            u=Template(name=form_template.name.data)
            db.session.add(u)
            db.session.commit()
            template_name='Template_'+u.name+'.txt'
            folder=os.environ.get('TEMPLATE_FOLDER')
            file= open(folder+template_name,'w')
            file.write('')
            return redirect(url_for('pyps.index'))

    return render_template('pyps/index.html',form=form,form_template=form_template)










