from bs4 import BeautifulSoup
from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, Category, Subcategory, Info, Hardware
from app.main.forms import EditProfileForm, PostForm, LocationForm, NetworkForm, CustomerForm, Post_r_Form, StatisticForm, DeleteForm, InfoForm,RemoveForm, StatbyTimeForm
from requests import Request, Session
import bs4 as bs
import pandas as pd
from app.data import bp
from flask_login import login_required, current_user
from flask_babel import _, get_locale
import os
import requests
from app import db
from app.models import Customer
from app.functions.sshcon import connector
from app.functions.charts import barchart, barchart_byTime
from app.edit.routes import delete
from datetime import date
from datetime import datetime
from app.file.routes import expynew, expy
from app.functions.get_journals import get_bo_journals
from flask import session


@bp.route('/scraper',methods=['GET', 'POST'])
@login_required



def scraper():
    contract=request.args.get('contract')
    login_url=os.environ.get('login_url_env')+contract
    
    username= os.environ.get('username_env')
    password = os.environ.get('password_env')
    pm=""
    out_vrf=""

    req = requests.get(login_url, auth=(username, password))
    final_page = bs.BeautifulSoup(req.content, 'lxml')
    #out=final_page.find_all('a', attrs={'class':'DetailInternalLink'})
    out_match= final_page.find('td', class_='DetailName', text='Match-Code').findNext('td', class_="DetailText")
    out_hardware=final_page.select_one("a[href*=hardware_show]")
    out_hardwaresn=final_page.select_one("a[href*=hardware_edit]")
    out_technology= final_page.find('td', class_='pl-4').findNext('div', class_="h2 mt-1")
    out_project= final_page.select_one("a[href*=project_show]")
    out_customer=final_page.find_all('a', class_='DetailInternalLink')
    out_customer=out_customer[0]
    out_seller= final_page.find('td', class_='DetailName', text='Verkäufer').findNext('td', class_="DetailText")
    out_sid= final_page.find('td', class_='DetailName', text='YAPS-UID').findNext('td', class_="DetailText")

    if out_hardware is not None:
       
        
        out_hardware=out_hardware.contents[0]
        out_hardware=out_hardware.strip()
        out_hardwaresn=out_hardwaresn.contents[0]
        out_hardwaresn=out_hardwaresn.strip()
        out_hardware=out_hardware+":"+out_hardwaresn

    
    if out_project is not None:
        
        pm=out_project.attrs['href']
        pm=pm[40:]
        print(pm)
        out_project=out_project.contents[0]
        
        login_url='https://intern.inode.at/backoffice/project/project_show.php4?Project_ID='+pm
        req = requests.get(login_url, auth=(username, password))
        pm_page = bs.BeautifulSoup(req.content, 'lxml')
        
        pm=pm_page.find('td', class_="PageViewHeader", text="Notiz").findNext('td').findNext('td')
        pm=pm.contents[0]
       


    login_url="https://intern.inode.at/backoffice/contract/contract_config_edit.php4?Contract_ID="+contract
    req = requests.get(login_url, auth=(username, password))
    edit_page = bs.BeautifulSoup(req.content, 'lxml')
    try:
        out_contact=edit_page.find('td', class_="PageViewHeader", text="Kontaktperson").findNext('input').attrs
        out_contact=out_contact['value']
    except:
        out_contact=""

    try:
        out_contact_tel=edit_page.find('td', class_="PageViewHeader", text="Kontaktperson (Tel)").findNext('input').attrs
        out_contact_tel=out_contact_tel['value']
    except:
        out_contact_tel=""
    if edit_page.find('td', class_="PageViewHeader", text="Kontaktperson (Tel)") is None:
        try:
            out_contact_tel=edit_page.find('td', class_="PageViewHeader", text="Telefonnummer (privat)").findNext('input').attrs
            out_contact_tel=out_contact_tel['value']
        except:
               out_contact_tel=""
    try:
        out_residence_street=edit_page.find('td', class_="PageViewHeader", text="Strasse").findNext('input').attrs
        out_residence_number=edit_page.find('td', class_="PageViewHeader", text="Hausnummer").findNext('input').attrs
        out_residence_plz=edit_page.find('td', class_="PageViewHeader", text="PLZ").findNext('input').attrs
        out_residence_city=edit_page.find('td', class_="PageViewHeader", text="Ort").findNext('input').attrs

        out_residence_street=out_residence_street['value']
        out_residence_number=out_residence_number['value']
        out_residence_plz=out_residence_plz['value']
        out_residence_city=out_residence_city['value']
        out_residence=out_residence_street+ " " + out_residence_number+ " ,"+ out_residence_plz+ " " + out_residence_city
    except:
        out_residence=out_match.contents[0]

    if edit_page.find('td', class_="PageViewHeader", text="VRF Name") is not None:
        out_vrf=edit_page.find('td', class_="PageViewHeader", text="VRF Name").findNext('input').attrs
        out_vrf=out_vrf['value']
    
    print(out_contact)   



    out_match=out_match.contents[0]
    out_seller=out_seller.contents[0]
    out_technology=out_technology.contents[0]
    out_technology=out_technology.strip()
    out_technology= " ".join(out_technology.split())
    print(out_customer.contents[0])
    out_customer=out_customer.contents[0]
    
    
    out_contact=out_contact+" Tel: " + out_contact_tel
    


        

    

    selcust=Customer.query.filter_by(name=out_customer).first()
    if selcust is not None:
        selcust=selcust.id

    if out_sid.contents is not None:
        try:
            out_sid=out_sid.contents[0]
        except:
            out_sid=""
    
        
    
        


   
    

        
    return json.dumps({"match": out_match,  "technology": out_technology, "hardware": out_hardware ,
        "customer" : out_customer, "selcust": selcust, "project": out_project, "pm": pm, "seller": out_seller,
        "sid": out_sid, "contact": out_contact,"residence": out_residence, "vrf": out_vrf

        });




@bp.route('/scripter',methods=['GET', 'POST'])
@login_required


def scripter():

    return



@bp.route('/statistics/<username>' ,methods=['GET', 'POST'])
@login_required
def statistics(username):
    date=datetime.today().strftime('%d-%m-%Y')
    form_del=DeleteForm()
    form_byTime=StatbyTimeForm()
    

    stats2=None

    if form_del.validate_on_submit():

        
        if form_del.delete.data:  
            print('form validate')
            id=form_del.id_del.data
            delete(Statistic,id)
            return redirect(url_for('data.statistics',username=current_user.username))

    user=User.query.filter_by(username=username).first_or_404()

    
    page = request.args.get('page', 1, type=int)

    stats = user.statistics.order_by(Statistic.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('data.statistics',username=current_user.username, page=stats.next_num) \
        if stats.has_next else None
    prev_url = url_for('data.statistics',username=current_user.username, page=stats.prev_num) \
        if stats.has_prev else None
    barchart()


    if form_byTime.validate_on_submit():
        print('Hallo')
        if form_byTime.submit.data:

            time=form_byTime.daterange.data
            
            time = time.split(" - ")
            start=time[0].split("/")
            endig=time[1].split("/")

           
            sm=start[0]
            sd=start[1]
            sy=start[2]
            
            em=endig[0]
            ed=endig[1]
            ey=endig[2]



            

            

            

            page = request.args.get('page', 1, type=int)
            stats=statistic_byTime(sm,sd,sy,em,ed,ey)
            stats=stats.order_by(Statistic.timestamp.desc())


            
    
               
            
                
            barchart_byTime(sm,sd,sy,em,ed,ey)
            return render_template('statistics.html', user=user, stats=stats, form_del=form_del,
                           form_byTime=form_byTime,date=date)



        if form_byTime.create.data:
                print('create_button)')

                time=form_byTime.daterange.data
            
                time = time.split(" - ")
                start=time[0].split("/")
                endig=time[1].split("/")

           
                sm=start[0]
                sd=start[1]
                sy=start[2]
                em=endig[0]
                ed=endig[1]
                ey=endig[2]

                page = request.args.get('page', 1, type=int)
                stats=statistic_byTime(sm,sd,sy,em,ed,ey)
                

                num=expynew(date)
                num=str(num)
                for i in stats:
                    expy(i.category.name,i.subcategory.name,i.hardware,i.user,i.technology,i.customer,i.contract,i.time,date,num)

                        
    
               
                stats=stats.filter(Statistic.user_id_stat==current_user.id).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
                next_url = url_for('data.statistics',username=current_user.username, page=stats.next_num) \
                    if stats.has_next else None
                prev_url = url_for('data.statistics',username=current_user.username, page=stats.prev_num) \
                    if stats.has_prev else None
                barchart_byTime(sm,sd,sy,em,ed,ey)
                download=True
                return render_template('statistics.html', user=user, stats=stats.items, form_del=form_del,next_url=next_url,
                           prev_url=prev_url,form_byTime=form_byTime,date=date,download=download,num=num)



             
        return render_template('statistics.html', user=user, stats=stats.items, form_del=form_del,next_url=next_url,
                           prev_url=prev_url,form_byTime=form_byTime,date=date,num=num)



          
        
                






             
                    

    


            

            

           
          
                    


    return render_template('statistics.html', user=user, stats=stats.items, form_del=form_del,next_url=next_url,
                           prev_url=prev_url,form_byTime=form_byTime,date=date)



def statistic_byTime(sm,sd,sy,em,ed,ey):
    print(sm,sd,sy,em,ed,ey)

    start=sm+"/"+sd+"/"+sy
    end=em+"/"+ed+"/"+ey
    
    objDatestart = datetime.strptime(start, '%m/%d/%Y')
    objDateend = datetime.strptime(end, '%m/%d/%Y')
    
    
    stats=Statistic.query.filter(Statistic.timestamp <= objDateend).filter(Statistic.timestamp >= objDatestart)

    

    return stats



@bp.route('/cors/<path:url>',methods=['GET', 'POST'])
@login_required

def cors(url):
    username=session['username']
    password=session['password']
    s=requests.Session()
    s.auth=(username,password)
    param_data={'sid': 'iB2B5728'}
    data=s.get(url, params=param_data).content
    

    return data


@bp.route('/bo_journals/<contract>',methods=['GET', 'POST'])
@login_required


def bo_journals(contract):

    dict_data_journal=get_bo_journals(contract)


    return json.dumps(dict_data_journal, ensure_ascii=False)





