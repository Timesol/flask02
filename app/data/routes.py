from bs4 import BeautifulSoup
from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from requests import Request, Session
import bs4 as bs
import pandas as pd
from app.data import bp
from flask_login import login_required
from flask_babel import _, get_locale
import os
import requests
from app import db
from app.models import Customer


@bp.route('/scraper',methods=['GET', 'POST'])
@login_required



def scraper():
    contract=request.args.get('contract')
    login_url=os.environ.get('login_url_env')+contract
    
    username= os.environ.get('username_env')
    password = os.environ.get('password_env')

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
        pm=pm.contents[2]
        pm=pm[6:]
        



    out_match=out_match.contents[0]
    out_technology=out_technology.contents[0]
    out_technology=out_technology.strip()
    out_technology= " ".join(out_technology.split())
    print(out_customer.contents[0])
    out_customer=out_customer.contents[0]

    selcust=Customer.query.filter_by(name=out_customer).first()
    if selcust is not None:
        selcust=selcust.id
    
        
    
        


   
    

        
    return json.dumps({"match": out_match,  "technology": out_technology, "hardware": out_hardware ,"customer" : out_customer, "selcust": selcust, "project": out_project, "pm": pm});