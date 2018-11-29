from bs4 import BeautifulSoup
import requests
from requests import Request, Session
import bs4 as bs
import pandas as pd
from app.data import bp
from flask_login import login_required
from flask_babel import _, get_locale



@bp.route('/scraper',methods=['GET', 'POST'])
@login_required



def scraper():
    contract=request.args.get('contract')
    login_url=os.environ.get('login_url_env')+contract
    login_url2=os.environ.get('login_url2_env')+contract
    username= os.environ.get('username_env')
    password = os.environ.get('username_env')

    req = requests.get(login_url2, auth=(username, password))
    final_page = bs.BeautifulSoup(req.content, 'lxml')
    #out=final_page.find_all('a', attrs={'class':'DetailInternalLink'})
    out_match= final_page.find('td', class_='DetailName', text='Match-Code').findNext('td', class_="DetailText")
    out_project= final_page.find('td', class_='DetailName', text='Projekt').findNext('td', class_="DetailText")
    out_project=out_project.findNext('a', class_='DetailInternalLink')
    out_technology= final_page.find('td', class_='pl-4').findNext('div', class_="h2 mt-1")
    out_hardware=final_page.select_one("a[href*=hardware_show]")
    out_customer=final_page.select_one("a[href*=client_show]")

    if out_hardware is not None:
        out_hardware=out_hardware.contents[0]
        out_hardware=out_hardware.strip()
    out_match=out_match.contents[0]
    if out_project is not None:
        out_project=out_project.contents[0]
    out_technology=out_technology.contents[0]
    out_technology=out_technology.strip()
    out_technology= " ".join(out_technology.split())
    out_customer=out_customer.contents[0]
    print(out_hardware)
    print(out_match)
    print(out_project)
    print(out_technology)
    print(out_customer)
        
    return json.dumps({'match': out_match, 'project': out_project, 'technology': out_technology, 'hardware': out_hardware});