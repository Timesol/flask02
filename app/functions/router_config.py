from app import db
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, \
Category, Subcategory, Info, Hardware, Template,Journal
from flask_login import current_user
from flask import render_template, flash, redirect, url_for, request, g, current_app, json



def create_config(contract,template_id):

	template=Template.query.get(template_id)
    
    
	config=render_template('router_configs/'+'Template_'+template.name+'.html', contract=contract)
	config=config.replace('\n', '<br />')

	return config




    

	