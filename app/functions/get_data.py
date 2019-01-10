import requests
from requests import Request, Session
from requests import get
from requests import post
from bs4 import BeautifulSoup
import bs4 as bs
from flask import session

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
    output=final_page.find_all('input' )
    dict_data={}
    for i in output:
        dict_data[i.attrs.get('name', 'NA')]= i.attrs.get('value', 'NA')
    dict_data.pop('NA')
    for i in dict_data:
        print(i + ' : ' + dict_data[i])
    

    return dict_data