import requests
from requests import Request, Session
from requests import get
from requests import post
from bs4 import BeautifulSoup
import bs4 as bs

username='ahoehne'
password='Katze7436!'
s=requests.Session()

s.auth=(username,password)
c=s.get('https://intern.inode.at/backoffice/contract/contract_config_edit.php4?Contract_ID=1463695')
data=s.get('https://intern.inode.at/backoffice/contract/contract_config_edit.php4?Contract_ID=1463695').content
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
print(dict_data)



'''
dict_data['Basisvar-net-network-1-net_name-1']='Testnetz'
login_url='https://intern.inode.at/backoffice/contract/contract_config_edit.php4?Contract_ID=1462885'
reqbody={'Action':'Config.Save',
'unlock':'true',
'PaymentSave':'alle+Konfigurationen+speichern',
'Basisvar-hardware-password-1':'Test'}


w=s.post(login_url,stream=True, data=dict_data
	,allow_redirects=True)
print(w.status_code) 
'''

    
    


