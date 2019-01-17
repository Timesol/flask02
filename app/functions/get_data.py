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
from collections import OrderedDict



def bo_ilvt(sid):
    link=os.environ.get('BO_ILVT_LINK')+'ProductGroup=&status=&findUnedited=current_only&excludeEdited=no&date=&days_of_state=0&date_search=estimated&Worker_ID=&sid=' + sid + '&Auftrag=&TASL=&cid=&adsl_nr=&ordertype=all&client_type=all&Action=Search&button=+++Suche+starten+++'
    print(sid)
    username=session['username']
    password=session['password']
    s=requests.Session()
    param_data={'sid': sid}
    s.auth=(username,password)
    c=s.get(link,params=param_data)
    s.cookies=c.cookies
    #s.headers=c.headers
    print(c.cookies)
    print(c.headers)
    print(c.status_code)
    final_page=bs.BeautifulSoup(c.content, 'lxml')
    output=final_page.find_all("img", src=lambda src: src and "orderstate" in src)
    
    dict_data_ilvt=OrderedDict()
    count=0
    items_dict_data_ilvt=len(output)
    for i in output:
       dict_data_ilvt['contract'+str(count)]=('Contract: '+ i.findNext('td', {'align': 'CENTER'}).text)
       dict_data_ilvt['sid'+str(count)]=('SID: '+i.findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).text)
       dict_data_ilvt['status'+str(count)]=('Status: '+i.findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).text)
       dict_data_ilvt['product'+str(count)]=('Product: '+i.findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).text)
       dict_data_ilvt['productcat'+str(count)]=('Productcategory: '+i.findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).text)
       dict_data_ilvt['customer'+str(count)]=('Customer: '+i.findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).text)
       dict_data_ilvt['node'+str(count)]=('Node: '+i.findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).text)
       dict_data_ilvt['line'+str(count)]=(str('Line: '+i.findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
        findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).get_text(separator='%%')))
       dict_data_ilvt['konzi'+str(count)]=('Konzi: '+i.findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).get_text(separator='%%'))
       dict_data_ilvt['slot'+str(count)]=('Slot: '+i.findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).get_text(separator='%%'))
       dict_data_ilvt['port'+str(count)]=('Port: '+i.findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).get_text(separator='%%'))
       dict_data_ilvt['slotname'+str(count)]=('Slotname: '+i.findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).get_text(separator='%%'))
       dict_data_ilvt['tasl'+str(count)]=('Tasl: '+i.findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).get_text(separator='%%'))
       dict_data_ilvt['ain'+str(count)]=('AIN/EIN: '+i.findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).findNext('td', {'align': 'CENTER'}).
            findNext('td', {'align': 'CENTER'}).get_text(separator='%%'))
       count+=1

    

    
    return dict_data_ilvt, items_dict_data_ilvt
      


        
    
        
    
        

    















def entries_to_remove(entries, dicto):
    for key in entries:
        if key in dicto:
            del dicto[key]

    return dicto
