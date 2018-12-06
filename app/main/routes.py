from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, PostForm, LocationForm, NetworkForm, CustomerForm, Post_r_Form, Statistic_Work_Form, DeleteForm
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, Category, Subcategory
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
from app.file.routes import expy




 

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




@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))



@bp.route('/cutomers',methods=['GET', 'POST'])
@login_required
def customers():
            
    available_customers=Customer.query.all()
    groups_list=[(i.id,i.name) for i in available_customers]
    form= LocationForm()
    form2= CustomerForm()

    form.customer.choices = groups_list
    if form.validate_on_submit():
        
        location = Location(residence=form.residence.data, technology=form.technology.data,
        hardware=form.hardware.data,project=form.project.data, projectmanager=form.projectmanager.data, contract= form.contract.data)

        db.session.add(location)
        
        customer=Customer.query.get(form.customer.data)
        customer.locations.append(location)
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.customers'))
    custquerys=Customer.query.all()
    locquerys=Location.query.all()

    if form2.validate_on_submit():
        custname=Customer(name=form2.name.data)
        db.session.add(custname)
        db.session.commit()
        flash(_('Your changes have been saved.'))
        
    return render_template('customers.html', title=_('Customers'), form=form, locquerys=locquerys, custquerys=custquerys, form2=form2)

@bp.route('/customersu/<customername>', methods=['GET', 'POST'])
@login_required

def customersu(customername):
    available_categorys=Category.query.all()
    category_list=[(i.id,i.name) for i in available_categorys]

    available_subcategorys=Subcategory.query.all()
    subcategory_list=[(i.id,i.name) for i in available_subcategorys]
   
    

    form=NetworkForm()
    form_work=Statistic_Work_Form()
    form_del=DeleteForm()


    if form_del.validate_on_submit():
        
        if form_del.delete.data:  
            print('form validate')
            id=form_del.id_del.data
            delete(Location,id)
            return redirect(url_for('main.customersu',customername=customername))

    form_work.category.choices=category_list
    form_work.subcategory.choices=subcategory_list
    
    

    cust = Customer.query.filter_by(name=customername).first_or_404()
    lists=cust.locations
    if form_work.validate_on_submit():
        statistic_db=Statistic(technology=form_work.technology.data, time=form_work.time.data,customer=form_work.customer.data, contract=form_work.contract.data,
            hardware=form_work.hardware.data, user=form_work.user.data)

        db.session.add(statistic_db)
        db.session.commit()
        user=User.query.filter_by(username=current_user.username).first()
        user.statistics.append(statistic_db)
        db.session.commit()

        category=Category.query.get(form_work.category.data)
        subcategory=Subcategory.query.get(form_work.subcategory.data)

        category.statistics.append(statistic_db)
        subcategory.statistics.append(statistic_db)
        db.session.commit()



        cat=form_work.category.data
        scat=Subcategory.query.get(form_work.subcategory.data).name
        cat=Category.query.get(form_work.category.data).name
        hard=form_work.hardware.data
        user=form_work.user.data
        tech=form_work.technology.data
        cust=form_work.customer.data
        contr=form_work.contract.data
        time=form_work.time.data

        
        expy(cat,scat,hard,user,tech,cust,contr,time)
        return redirect(url_for('main.customersu',customername=customername))
    
     
    if form.validate_on_submit():
        
        
        location=Location.query.get(form.locid.data)

       
        networklist= Network(network=form.network.data, name=form.name.data, fromip=form.fromip.data, toip=form.toip.data,

        gateway=form.gateway.data,subnet=form.subnet.data,cdir=form.cdir.data,vip=form.vip.data)
        
        location.networks.append(networklist)
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.customersu',customername=customername))
    
        count=0
    if request.args.get('list'): 
        no=request.args.get('list')
        location=Location.query.get(no)
        k=0
        a={}
        t=0
        for i in location.networks:
            if i == None:
                break
            key=k
            value= i.name
            a[key]= value
            k+=1
        for i in range(0,k,1):
            print(a[t])
            t+=1   
            

        return json.dumps({'id': a });   




        


    return render_template('customersu.html', cust=cust, lists=lists, form=form, form_work=form_work, form_del=form_del)
    



@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)



@bp.route('/edit',methods=['GET', 'POST'])
@login_required

def edit():
       
    var1 = request.args.get('var1',None)
    arg=Location.query.get(var1)
    available_customers=Customer.query.all()
    groups_list=[(i.id,i.name) for i in available_customers]
    form= LocationForm()
    form.customer.choices = groups_list



    if form.validate_on_submit():
        arg.residence=form.residence.data
        arg.project=form.project.data
        arg.projectmanager=form.projectmanager.data
        arg.hardware=form.hardware.data
        arg.technology=form.technology.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
    return render_template('edit.html', title=_('Edit'), arg=arg, form=form )




@bp.route('/router',methods=['GET', 'POST'])
@login_required


def router():
    form = Post_r_Form()
    if form.validate_on_submit():
        #check language of post 
        language = guess_language(form.post_r.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''

        post_r = Post_r(body=form.post_r.data,author_r=current_user ,language=language)
        db.session.add(post_r)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('main.router'))





    page = request.args.get('page', 1, type=int)
    posts_r = Post_r.query.order_by(Post_r.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.router', page=posts_r.next_num) \
        if posts_r.has_next else None
    prev_url = url_for('main.router', page=posts_r.prev_num) \
        if posts_r.has_prev else None


    return render_template('router.html', title=_('Router') ,posts_r=posts_r.items, next_url=next_url,
                           prev_url=prev_url, form=form)


@bp.route('/router_todo',methods=['GET', 'POST'])
@login_required


def router_todo():
    no=request.args.get('no')

    location=Location.query.get(no)
    post=render_template('router_todo.txt', location=location)
    add_post=Post_r(body=post, author_r=current_user)
    db.session.add(add_post)
    db.session.commit()


    return json.dumps({'status':'OK'});




@bp.route('/statistics/<username>')
@login_required
def statistics(username):
    user=User.query.filter_by(username=username).first_or_404()
    stats=user.statistics



    return render_template('statistics.html', user=user, stats=stats)














@bp.route('/save',methods=['GET', 'POST'])
@login_required



def save():
    no=request.args.get('no')
    new_residence = request.args.get('residence_val', None)
    new_project = request.args.get('project_val', None)
    new_projectmanager = request.args.get('projectmanager_val', None)
    new_hardware = request.args.get('hardware_val', None)
    new_technology = request.args.get('technology_val', None)
    new_contract = request.args.get('contract_val', None)
    
   
    arg=Location.query.get(no)
    arg.residence=new_residence
    arg.project=new_project
    arg.projectmanager=new_projectmanager
    arg.hardware=new_hardware
    arg.technology=new_technology
    arg.contract=new_contract
    db.session.commit()


    return json.dumps({'status':'OK'});





def delete(table, id):
    print('It works')

    object = table.query.get(id)
    db.session.delete(object)
    db.session.commit()
    flash('Object deleted')


@bp.route('/contract/<id>',methods=['GET', 'POST'])
@login_required

def contract(id):

    contract=Location.query.get(id)

    return render_template('contract.html', contract=contract)


































''' @bp.route('/query',methods=['GET', 'POST'])
@login_required

def query():
    no=request.args.get('no')

    location=Location.query.get(no)
    d={}
    for i in location.networks:
        netid='network'+ str(i.id)
        netid=str(netid)
        id= 'id'+ str(i.id)
        print(netid)
        a={
        id : i.name,
        netid : i.network}
        d.update(a)

    
    print (d)

    locr=location.residence
    locp=location.project
    locpm=location.projectmanager  
    loch=location.hardware
    loct=location.technology
    locc=location.contract
    d1={'locr':locr,'locp':locp,'locpm':locpm,'loch':loch,'loct':loct,'locc':locc, }
    d2=d
    d1.update(d2)
    
    return json.dumps(d1); '''












