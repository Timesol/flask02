from flask import render_template, flash, redirect, url_for, request, g, current_app, json
import requests
from requests import Request, Session
from requests import get
from requests import post
from bs4 import BeautifulSoup
import bs4 as bs
from flask import session
from flask import Markup
import os
import time



def get_bo_journals(contract):
    print('in Function')
    dict_data_journal={}
    dict_data_name={}
    dict_data_date={}
    
    link=os.environ.get('BO_SHOW_LINK')+str(contract)
   
    username=session['username']
    password=session['password']
    s=requests.Session()
    param_data={'rowShow3':'0'}
    s.auth=(username,password)
    c=s.get(link,params=param_data)
    s.cookies=c.cookies
    #s.headers=c.headers
    print(c.cookies)
    print(c.headers)
    print(c.status_code)

    final_page = bs.BeautifulSoup(c.content, 'lxml')
    output=final_page.find_all("a", href=lambda href: href and "journal_show" in href,class_='PageViewDataLink')
   

    

    selkeys=list()
    
    for i in output:
        

        j=i.text
        k=i.attrs.get('href')
        k=k[2::]
        k='https://intern.inode.at/backoffice/'+k
        dict_data_journal[k]=j
        dict_data_name[k]=i.findNext('td').findNext('td').text
        dict_data_date[k]=i.findNext('td').findNext('td').findNext('td').findNext('td').text
    	
    

    for (key , value) in dict_data_journal.items():
    	if 'Feedback REGRADE' in value:
    		selkeys.append(key)
    
    for key in selkeys:
    	if key in dict_data_journal:
    		del dict_data_journal[key]


    
    return dict_data_journal, dict_data_name, dict_data_date

