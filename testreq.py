import requests

payload = {'inUserName': 'ahoehne', 'inUserPass': 'Hund338!'}
url = 'https://intern.inode.at/backoffice/extras/overview.php4'
requests.post(url, data=payload)
