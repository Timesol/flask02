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
    output=final_page.find_all('tr' )

    dict_data={}
    for i in output:
        if i is not None:
            j=i.find('input')
            i=i.find('td', class_='PageViewHeader')
        dict_data[i]=j
        dict_data.pop(None)

    for i in dict_data:
        print(i)
        print(dict_data.get(i))

   
        


    

            
            
          
        
        
        

    



 
   
    

    return dict_data


def entries_to_remove(entries, dicto):
    for key in entries:
        if key in dicto:
            del dicto[key]

    return dicto