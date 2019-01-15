from flask import render_template, flash, redirect, url_for, request, g, current_app, json
import requests
from requests import Request, Session
from requests import get
from requests import post
from bs4 import BeautifulSoup
import bs4 as bs
from flask import session
from flask import Markup



def bo_ilvt(sid):

    username=session['username']
    password=session['password']
    s=requests.Session()
    link==os.environ.get('BO_SHOW_LINK')+str(sid)
    s.auth=(username,password)
    c=s.get(link)
    
    s.cookies=c.cookies
    #s.headers=c.headers
    print(c.cookies)
    print(c.headers)
    print(c.status_code)
    final_page = bs.BeautifulSoup(c.content, 'lxml')













def entries_to_remove(entries, dicto):
    for key in entries:
        if key in dicto:
            del dicto[key]

    return dicto
