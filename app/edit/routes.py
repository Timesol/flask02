from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from app.edit import bp
from flask_login import login_required
from app import db
from app.models import Customer,Location,Network,User,Statistic

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
    new_hardware=new_hardware.split(":")

    
    
   
    arg=Location.query.get(no)
    arg.residence=new_residence
    arg.project=new_project
    arg.projectmanager=new_projectmanager
    arg.hardware.first().name=new_hardware[0]
    arg.hardware.first().sn=new_hardware[1]
    arg.technology=new_technology
    arg.contract=new_contract
    db.session.commit()


    


    return json.dumps({'status':'OK'});



@bp.route('/save_net',methods=['GET', 'POST'])
@login_required



def save_net():
    no=request.args.get('no')
    no_loc=request.args.get('no_loc')
    print(no)
    print(no_loc)
    new_network = request.args.get('network_val', None)
    new_gateway = request.args.get('gateway_val', None)
    new_subnet = request.args.get('subnet_val', None)
    new_cdir = request.args.get('cdir_val', None)
    new_vip = request.args.get('vip_val', None)

    arg_net=Network.query.get(int(no))
   
    

    arg_net.network=new_network
    arg_net.gateway=new_gateway
    arg_net.subnet=new_subnet
    arg_net.cdir=new_cdir
    arg_net.vip=new_vip
    db.session.commit()
    

    return json.dumps({'status':'OK'});






def delete(table, id):
    print('It works')

    object = table.query.get(id)
    db.session.delete(object)
    db.session.commit()
    flash('Object deleted')
