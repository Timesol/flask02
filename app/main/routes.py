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
from app.functions.get_journals import get_bo_journals
from datetime import datetime
import inspect
import wtforms
from sqlalchemy.inspection import inspect
from app.functions.save_db import add_cols





@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())






@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        #check language of post 
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''

        post = Post(body=form.post.data, author=current_user, language=language)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)



@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    location, total=Location.search(g.search_form.q.data,page,current_app.config['POSTS_PER_PAGE'])
    loc=location.first()

    available_customers=Customer.query.all()
    customer_list=[(i.id,i.name) for i in available_customers]

    
    

    
    
    form= LocationForm()
    form.customer.choices = customer_list
    if form.validate_on_submit():
            
            location = Location(residence=form.residence.data, technology=form.technology.data,
            project=form.project.data, projectmanager=form.projectmanager.data, contract= form.contract.data,contact=form.contact.data,
            vrf=form.vrf.data,seller=form.seller.data,sid=form.sid.data,matchcode=form.matchcode.data)
    
            if form.hardware.data:
                hardware=form.hardware.data
                hardware=hardware.split(":")
                hardware=Hardware(name=hardware[0], sn=hardware[1])
                db.session.add(hardware)
                location.hardware.append(hardware)
            db.session.commit()
            db.session.add(location)
            customer=Customer.query.get(form.customer.data)
            customer.locations.append(location)
            db.session.commit()
            flash(_('Your changes have been saved!'))
            return redirect(url_for('main.contract',id=location.id))

    if loc is not None:
        return redirect(url_for('main.contract',id=loc.id))


    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,location=location,
                           next_url=next_url, prev_url=prev_url, form=form)



@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)



@bp.route('/customers',methods=['GET', 'POST'])
@login_required
def customers():

    form= CustomerForm()
    custquerys=Customer.query.all()
    

    if form.validate_on_submit():




        custname=Customer(name=form.name.data)
        db.session.add(custname)
        db.session.commit()





        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.locations',customername=custname.name))

    return render_template('customers.html', title=_('Customers'), custquerys=custquerys, form=form)



@bp.route('/locations/<customername>', methods=['GET', 'POST'])
@login_required

def locations(customername):
    customer = Customer.query.filter_by(name=customername).first_or_404()
    locations=customer.locations

    available_customers=Customer.query.all()
    customer_list=[(i.id,i.name) for i in available_customers]

    available_categorys=Category.query.all()
    category_list=[(i.id,i.name) for i in available_categorys]

    available_subcategorys=Subcategory.query.all()
    subcategory_list=[(i.id,i.name) for i in available_subcategorys]
   
    form= LocationForm()
    form_stat=StatisticForm()
    form_del=DeleteForm()
    
    form.customer.choices = customer_list
    form_stat.category.choices=category_list
    form_stat.subcategory.choices=subcategory_list
    
    if form_del.validate_on_submit():
        if form_del.delete.data:  
            id=form_del.id_del.data
            delete(Location,id)
            return redirect(url_for('main.locations',customername=customername))

    
    if form_stat.validate_on_submit():


        add_cols(Statistic, form_stat, User, Category, Subcategory)

        
        return redirect(url_for('main.locations',customername=customername))


    
    if form.validate_on_submit():
        
        location = Location(residence=form.residence.data, technology=form.technology.data,
        project=form.project.data, projectmanager=form.projectmanager.data, contract= form.contract.data,contact=form.contact.data,
        vrf=form.vrf.data,seller=form.seller.data,sid=form.sid.data,matchcode=form.matchcode.data)

        if form.hardware.data:
            hardware=form.hardware.data
            hardware=hardware.split(":")
            hardware=Hardware(name=hardware[0], sn=hardware[1])
            db.session.add(hardware)
            location.hardware.append(hardware)
        db.session.commit()
        db.session.add(location)
        customer=Customer.query.get(form.customer.data)
        customer.locations.append(location)
        db.session.commit()
        flash(_('Your changes have been saved!'))
        return redirect(url_for('main.contract',id=location.id))

    return render_template('locations.html', customer=customer, locations=locations,form_stat=form_stat, form_del=form_del, form=form)
    


@bp.route('/router',methods=['GET', 'POST'])
@login_required


def router():
    form = Post_r_Form()
    form_byTime=RouterbyTimeForm()
    if form.validate_on_submit():

        post_r = Post_r(body=form.post_r.data,author_r=current_user)
        db.session.add(post_r)
        db.session.commit()
        flash(_('Routerinfos saved!'))
        return redirect(url_for('main.router'))

    if form_byTime.validate_on_submit():
        if form_byTime.show.data:
            time=form_byTime.daterange.data
            status=form_byTime.status.data
            npl=form_byTime.npl.data
            time = time.split(" - ")
            start=time[0].split("/")
            endig=time[1].split("/")
            sm=start[0]
            sd=start[1]
            sy=start[2]
            em=endig[0]
            ed=endig[1]
            ey=endig[2]

            routers=router_byTime(sm,sd,sy,em,ed,ey,status,npl)
            routers=routers.order_by(Post_r.timestamp.desc())
            return render_template('router.html', title=_('Router') ,posts_r=routers, 
                            form=form, form_byTime=form_byTime)


    page = request.args.get('page', 1, type=int)
    posts_r = Post_r.query.order_by(Post_r.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.router', page=posts_r.next_num) \
        if posts_r.has_next else None
    prev_url = url_for('main.router', page=posts_r.prev_num) \
        if posts_r.has_prev else None


    return render_template('router.html', title=_('Router') ,posts_r=posts_r.items, next_url=next_url,
                           prev_url=prev_url, form=form, form_byTime=form_byTime)


@bp.route('/router_todo',methods=['GET', 'POST'])
@login_required


def router_todo():
    no=request.args.get('no')

    location=Location.query.get(no)
    post=render_template('router_todo.txt', location=location)
    post=str(post)
    
    add_post=Post_r(body=post, author_r=current_user)
    db.session.add(add_post)
    db.session.commit()


    return json.dumps({'status':'OK'});




@bp.route('/contract/<id>',methods=['GET', 'POST'])
@login_required

def contract(id):
    dict_data={}
    dict_data_journal={}
    contract=Location.query.get(id)
    infos_t=contract.infos
    
    available_scripts=Script.query.all()
    scripts_list=[(i.id,i.name) for i in available_scripts]

    available_templates=Template.query.all()
    templates_list=[(i.id,i.name) for i in available_templates]

    available_categorys=Category.query.all()
    category_list=[(i.id,i.name) for i in available_categorys]

    available_subcategorys=Subcategory.query.all()
    subcategory_list=[(i.id,i.name) for i in available_subcategorys]


    form=NetworkForm()
    form_del=DeleteForm()
    form_info=InfoForm()
    form_remove=RemoveForm()
    form_script=ScriptForm()
    form_template=TemplateForm()
    form_get_nets=GetNetworksForm()
    form_journal=JournalForm()
    form_router=RouterForm()
    form_stat=StatisticForm()

    
    form_script.script.choices=scripts_list
    form_template.name.choices=templates_list
    form_stat.category.choices=category_list
    form_stat.subcategory.choices=subcategory_list

    if form_get_nets.validate_on_submit():
        if form_get_nets.get.data:
            link=os.environ.get('BO_CONFIG_LINK')+str(contract.contract)
            id=str(contract.id)
            dict_data=bo_data(link,id)
            

    if form_template.validate_on_submit():
        if form_template.submit.data:
            template=Template.query.get(form_template.name.data)
            u=Journal(description=template.name,user_j=current_user)
            db.session.add(u)
            db.session.commit()
            link=os.environ.get('JOURNAL_FOLDER')+'journal_show_'+str(u.id)+'.html'
            u.link=link
            contract.journals.append(u)
            db.session.commit()
            file= open(link,'w')
            config = create_config(contract,form_template.name.data)
            file.write(config)

            
            return redirect(url_for('main.router_config',journal_id=u.id))



    if form_remove.validate_on_submit():
        if form_remove.remove.data:
            info=Info.query.get(form_remove.id_rem.data)
            contract.remove_info(info)
            db.session.commit()
            return redirect(url_for('main.contract',id=contract.id))


    if form_del.validate_on_submit():
        
        if form_del.delete.data:  
            print('form validate')
            id=form_del.id_del.data
            delete(Network,id)
            return redirect(url_for('main.contract',id=contract.id))

    

    if form.validate_on_submit():
        if form.submit.data:
            

            networklist= Network(network=form.network.data, name=form.name.data, fromip=form.fromip.data, toip=form.toip.data,

            gateway=form.gateway.data,subnet=form.subnet.data,cdir=form.cdir.data,vip=form.vip.data)

            contract.networks.append(networklist)
            db.session.commit()
            flash(_('Your changes have been saved.'))

            return redirect(url_for('main.contract',id=contract.id, contract=contract))
    


    if form_info.validate_on_submit():

        if form_info.submit2.data:
            print(form_info.infotext.data)
            info_db=Info(infotext=form_info.infotext.data)
            print(infos_t)
            contract.infos.append(info_db)
            
            db.session.commit()
            flash(_('Your changes have been saved.'))
            return redirect(url_for('main.contract',id=contract.id, contract=contract, infos_t=infos_t))

    if form_script.validate_on_submit():

        if form_script.send.data:
            script_id=form_script.script.data
            script_name=Script.query.get(script_id).name
            script_name='Script_'+script_name+'.txt'
            script=render_template('scripts/'+script_name, contract=contract)
            connector_var=form_script.connector.data
            result=if_connector(connector_var,script)  
            findresult=result.find('terminal length 0')
            result=result[findresult::]
            print ('Ergebnis '+ result)
            flash(_('Script successfull finished!'))

        return redirect(url_for('main.contract',id=contract.id, contract=contract, infos_t=infos_t))

  
    

    if form_journal.validate_on_submit():
        if form_journal.submit_journal.data:
            u=Journal(description=form_journal.description.data,user_j=current_user)
            db.session.add(u)
            db.session.commit()
            link=os.environ.get('JOURNAL_FOLDER')+'journal_show_'+str(u.id)+'.html'
            u.link=link
            contract.journals.append(u)
            db.session.commit()
            file= open(link,'w')
            file.write(form_journal.body.data)

            return redirect(url_for('main.contract',id=contract.id, contract=contract))
    
    if form_router.validate_on_submit():
        if form_router.submit_router.data:

            location=Location.query.get(contract.id)
            post=render_template('router_todo.txt', location=location)
            post=str(post)
            
            
            if form_router.file.data:
                print(form_router.file.data.filename)
                date=datetime.today().strftime('%d-%m-%Y')
                
                UPLOAD_FOLDER_CONFIGS=os.environ.get('UPLOAD_FOLDER_CONFIGS')
                f =form_router.file.data
                filename = secure_filename(f.filename)
                filename=filename.split('.')
                filename=filename[0]+'_'+date+'.'+filename[1]
                f.save(os.path.join(UPLOAD_FOLDER_CONFIGS, filename))
                add_post=Post_r(body=post, author_r=current_user, npl=form_router.npl.data, status=form_router.status.data,filename=filename)
            else:
                add_post=Post_r(body=post, author_r=current_user, npl=form_router.npl.data, status=form_router.status.data)
            db.session.add(add_post)
            db.session.commit()


    if form_stat.validate_on_submit():
         if form_stat.save.data:
            statistic_db=Statistic(technology=form_stat.technology.data, time=form_stat.time.data,customer=form_stat.customer.data, contract=form_stat.contract.data,
                hardware=form_stat.hardware.data, user=form_stat.user.data)
    
            db.session.add(statistic_db)
            db.session.commit()
            user=User.query.filter_by(username=current_user.username).first()
            user.statistics.append(statistic_db)
            category=Category.query.get(form_stat.category.data)
            subcategory=Subcategory.query.get(form_stat.subcategory.data)
    
            category.statistics.append(statistic_db)
            subcategory.statistics.append(statistic_db)
            db.session.commit()
    
            cat=form_stat.category.data
            scat=Subcategory.query.get(form_stat.subcategory.data).name
            cat=Category.query.get(form_stat.category.data).name
            hard=form_stat.hardware.data
            user_data=form_stat.user.data
            tech=form_stat.technology.data
            cust=form_stat.customer.data
            contr=form_stat.contract.data
            time=form_stat.time.data
            now = datetime.today().strftime('%d-%m-%Y')
            
            return redirect(url_for('main.contract',id=contract.id))




    


    page = request.args.get('page', 1, type=int)
    journs = contract.journals.order_by(Journal.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.contract',id=contract.id, page=journs.next_num) \
        if journs.has_next else None
    prev_url = url_for('main.contract',id=contract.id, page=journs.prev_num ) \
        if journs.has_prev else None

    return render_template('contract.html',form_script=form_script, contract=contract, 
        form=form, form_del=form_del, form_info=form_info, infos_t=infos_t, form_remove=form_remove,
        form_template=form_template,journs=journs.items, form_journal=form_journal,next_url=next_url,
        prev_url=prev_url,form_get_nets=form_get_nets,dict_data=dict_data,form_router=form_router,
        form_stat=form_stat)


@bp.route('/append_all',methods=['GET', 'POST'])
@login_required


def append_all():
    i=request.args.get('info')
    c=request.args.get('customer')
    info=Info.query.get(i)

    customer=Customer.query.get(c)
    locations=Location.query.all()

    for f in locations:

       f.infos.append(info)
       db.session.commit()
      

    return json.dumps({'status':'OK'});



@bp.route('/append_info',methods=['GET', 'POST'])
@login_required


def append_info():
    i=request.args.get('info')
    c=request.args.get('customer')
    info=Info.query.get(i)

    customer=Customer.query.get(c)

    for f in customer.locations:


      f.infos.append(info)
    db.session.commit()

    return json.dumps({'status':'OK'});


@bp.route('/journal_show/<id>',methods=['GET', 'POST'])
@login_required


def journal_show(id):

    journ=Journal.query.get(id)
    journ_id=str(journ.id)
    return render_template('journal.html',journ=journ,journ_id=journ_id)



@bp.route('/router_config/<journal_id>',methods=['GET', 'POST'])
@login_required


def router_config(journal_id):
    journ=Journal.query.get(journal_id)
    journ_id=str(journ.id)


    return render_template('router_config.html',journ=journ, journ_id=journ_id)


@bp.route('/bo_nets/<id>',methods=['GET', 'POST'])
@login_required
def bo_nets(id):

    contract=Location.query.get(id)
    link=os.environ.get('BO_CONFIG_LINK')+str(contract.contract)
    id=str(contract.id)
    username='ahoehne'
    password='Katze7436!'
    s=requests.Session()

    s.auth=(username,password)
    c=s.get(link)
    data=s.get(link).content
    s.cookies=c.cookies
    #s.headers=c.headers
    print(c.cookies)
    print(c.headers)
    print(c.status_code)
    final_page = bs.BeautifulSoup(c.content, 'lxml')
    output=final_page.find_all('tr')
    output2=final_page.find_all(attrs={'name':True})
    output3=final_page.find_all(attrs={'selected':True})
    dict_data_send=OrderedDict()
    dict_data=OrderedDict()
    dict_data_tag=OrderedDict()

    for i in output2:
        dict_data_send[i.attrs.get('name')]=i.attrs.get('value', '')
    
    for i in output3:
        dict_data_send[i.parent.attrs.get('name')]=i.attrs.get('value', '')
    try:
        dict_data_send.pop('edit')
    except:
        print('Exception')

    

    
    
    for k in output:
        r=k.find('input')
        if r is not None:
            dict_data_send[(r.attrs.get('name'))]=r.attrs.get('value')
        v=k.find('textarea')
        if v is not None:
            dict_data_send[v.attrs.get('name')]=v.text


        
      
        i=k.find('td', class_='PageViewHeader')
        if i is not None:
            j=i.find_next_sibling().find_next_sibling().find('input')
            if j is not None:
                
                dict_data[j.attrs.get('name')+'%%'+ i.text]=j.attrs.get('value')
                dict_data_tag[j.attrs.get('name')+'%%'+ i.text]=j.attrs.get('name')

    entries_to_remove(entries, dict_data)



    test=[key for key, value in dict_data.items() if 'Netz(' in key]
    list_count=list()
    for i in test:
        list_count.append(list(dict_data.keys()).index(i))
    if len(list_count)==0:
        list_count.append(1)


    number_nets=len(list_count)*10+4
    print(number_nets)
    





    
    tech=contract.technology
    

    class MyForm(FlaskForm):
        name = StringField('static field')
        send = SubmitField('Submit')
        add= SubmitField('Add Network')

    

# add dynamic fields
    for key, value in dict_data.items():
        setattr(MyForm, key, StringField(default=value))

    form=MyForm()

    if form.validate_on_submit():
        if form.send.data:
            print('button not pressed')
            for key, value in dict_data.items():
                key2=key.split('%%')[0]
                dict_data_send[key2]=getattr(form, key).data
            for i in dict_data_send:
                try:
                    print(i + " " + dict_data_send.get(i, ''))

                except:
                    print('Exception reached')
                    dict_data_send.pop(i)
                    print(dict_data_send.get(i, ''))
            s.post(link, data=dict_data_send)
            flash(_('Config saved!'))
            return redirect(url_for('main.contract',id=contract.id))
    
        if form.add.data:
            print('button pressed')
            param_data={'Contract_ID': contract.contract,
            'Action':'addNetwork' ,'addNetworkType':'net_mpls'}
             
            for key, value in dict_data.items():
                print(getattr(form, key).data)
                key2=key.split('%%')[0]
                dict_data_send[key2]=getattr(form, key).data
            s.post(link, params=param_data, data=dict_data_send)
            
            flash(_('Network added!'))
            return redirect(url_for('main.bo_nets',id=contract.id))

    return render_template('bo_nets.html', dict_data=dict_data, 
        dict_data_tag=dict_data_tag,tech=tech,form=form, 
        contract=contract,list_count=list_count,number_nets=number_nets)
        

def entries_to_remove(entries, dict_data):
    for key in entries:
        if key in dict_data:
            del dict_data[key]




@bp.route('/bo_journals/<contract>',methods=['GET', 'POST'])
@login_required


def bo_journals(contract):
    try:

        dict_data_journal, dict_data_name, dict_data_date=get_bo_journals(contract)


        return render_template('bo_journals.html',dict_data_journal=dict_data_journal
            ,dict_data_name=dict_data_name, dict_data_date=dict_data_date,contract=contract)

    except:
        print('Exception')
        return render_template('blank.html')


@bp.route('/bo_ilvt_view/<contract>',methods=['GET', 'POST'])
@login_required




def bo_ilvt_view(contract):
    contract=Location.query.get(contract)
    try:
        dict_data_ilvt, items_dict_data_ilvt=bo_ilvt(contract.sid)
        return render_template('bo_ilvt.html',dict_data_ilvt=dict_data_ilvt,
        items_dict_data_ilvt=items_dict_data_ilvt)

    except:
        return render_template('blank.html')



def router_byTime(sm,sd,sy,em,ed,ey,status,npl):
    print(sm,sd,sy,em,ed,ey)

    start=sm+"/"+sd+"/"+sy
    end=em+"/"+ed+"/"+ey
    
    objDatestart = datetime.strptime(start, '%m/%d/%Y')
    objDateend = datetime.strptime(end, '%m/%d/%Y')
    
    if status =='all' and npl=='all':
        routers=Post_r.query.filter(Post_r.timestamp <= objDateend).filter(Post_r.timestamp >= objDatestart)
    elif status =='all' and npl !='all':
        
        routers=Post_r.query.filter(Post_r.timestamp <= objDateend).filter(Post_r.timestamp >= objDatestart).filter(Post_r.npl==npl)
    elif status !='all' and npl =='all':
        
        routers=Post_r.query.filter(Post_r.timestamp <= objDateend).filter(Post_r.timestamp >= objDatestart).filter(Post_r.status==status)    
    else:
        routers=Post_r.query.filter(Post_r.timestamp <= objDateend).filter(Post_r.timestamp >= objDatestart).filter(Post_r.npl==npl,Post_r.status==status)
        



    

    return routers



@bp.route('/add_journals/<contract>',methods=['GET', 'POST'])
@login_required




def add_journals(contract):
    
    return render_template('add_journal.html', contract=contract)












    


































