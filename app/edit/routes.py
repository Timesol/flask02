from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from app.edit import bp
from flask_login import login_required
from app import db
from app.models import Customer,Location,Network,User,Statistic,Hardware,Post_r

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
    new_sn=request.args.get('sn_val', None)
    
    new_contact = request.args.get('contact_val', None)
    new_seller = request.args.get('seller_val', None)
    new_matchcode= request.args.get('matchcode_val', None)
    new_vrf = request.args.get('vrf_val', None)
    new_sid = request.args.get('sid_val', None)
    new_connector = request.args.get('connector_val', None)

    
    
   
    arg=Location.query.get(no)
    print(arg.residence)
    arg.residence=new_residence
    arg.project=new_project
    arg.projectmanager=new_projectmanager
    if new_hardware is not None:
        if arg.hardware.first() is not None:
            arg.hardware.first().name=new_hardware
            arg.hardware.first().sn=new_sn
        else:
            u=Hardware(name=new_hardware, sn=new_sn)
            db.session.add(u)
            arg.hardware.append(u)
            db.session.commit()
    arg.technology=new_technology
    arg.contract=new_contract
    arg.contact=new_contact
    arg.seller=new_seller
    arg.matchcode=new_matchcode
    arg.vrf=new_vrf
    arg.sid=new_sid
    arg.connector=new_connector
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



# Still used ????

@bp.route('/paste_location',methods=['GET', 'POST'])
@login_required

def paste_location():
       
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



@bp.route('/save_status',methods=['GET', 'POST'])
@login_required


def save_status():
     id=request.args.get('id')
     status=request.args.get('status')
     print(status)
     post=Post_r.query.get(id)
     post.status=status
     db.session.commit()

     return json.dumps({'status':'ok'})
