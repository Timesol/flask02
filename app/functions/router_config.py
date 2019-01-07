from app import db
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, \
Category, Subcategory, Info, Hardware, Template,Journal
from flask_login import current_user



def create_config(contract,template_id):

	template=Template.query.get(template_id)
    
    
	config=render_template('router_configs/'+template'.txt', contract=contract)


def create_template(id):

    

	u=Template(name=form_template.name.data)
	db.session.add(u)
	db.session.commit()