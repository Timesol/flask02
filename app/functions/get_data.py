from flask import render_template, flash, redirect, url_for, request, g, current_app, json
import requests
from requests import Request, Session
from requests import get
from requests import post
from bs4 import BeautifulSoup
import bs4 as bs
from flask import session
from flask import Markup





def bo_data(link,id):

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
    output=final_page.find_all('tr' )

    dict_data={}
    dict_data_tag={}
    for i in output:
        if i is not None:
            j=i.find('input')
            i=i.find('td', class_='PageViewHeader')
            if j and i is not None:

               dict_data[i.text]=j.attrs.get('value')
               dict_data_tag[i.text]=j.attrs.get('name')
        

    for i in dict_data:
        print(i)
        print(dict_data.get(i))



    file='/home/ahoehne/flask01/app/templates/bo_nets.html'
    page=render_template('_bo_nets.html', dict_data=dict_data, dict_data_tag=dict_data_tag)
    
    file= open(file,'w')
    file.write(page)

   
    return dict_data


def entries_to_remove(entries, dicto):
    for key in entries:
        if key in dicto:
            del dicto[key]

    return dicto