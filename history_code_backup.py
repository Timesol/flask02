'''
Test paramiko, pxssh etc.




try:
    s = pxssh.pxssh()
    hostname = input('hostname: ')
    username = input('username: ')
    password = getpass.getpass('password: ')
    s.login(hostname, username, password)
    s.sendline('eval "{ sleep 1; echo username; sleep 1; echo password; sleep 1; echo df; sleep 5; }" | telnet 192.168.0.136') 
    s.prompt()             
    print(s.before)        
   
    
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)

'''



'''





import threading, paramiko
import paramiko as ssh
 

class ssh:
    shell = None
    client = None
    transport = None
 
    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)
 
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()
 
    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()
 
    def openShell(self):
        self.shell = self.client.invoke_shell()
 
    def sendShell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")
 
    def process(self):
        global connection
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = str(alldata, "utf8")
                strdata.replace('\r', '')
                print(strdata, end = "")
                if(strdata.endswith("$ ")):
                    print("\n$ ", end = "")


    def sendCommand(self, command):
        if(self.client):
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata
 
                    print(str(alldata, "utf8"))
        else:
            print("Connection not opened.")



 
 
sshUsername = "ahoehne"
sshPassword = "net7toor"
sshServer = "192.168.0.192"
 
 
connection = ssh(sshServer, sshUsername, sshPassword)
connection.openShell()
while True:
    command = input('$ ')
    if command.startswith(" "):
        command = command[1:]
    connection.sendShell(command)





    





'''





''' @bp.route('/query',methods=['GET', 'POST'])
@login_required

def query():
    no=request.args.get('no')

    location=Location.query.get(no)
    d={}
    for i in location.networks:
        netid='network'+ str(i.id)
        netid=str(netid)
        id= 'id'+ str(i.id)
        print(netid)
        a={
        id : i.name,
        netid : i.network}
        d.update(a)

    
    print (d)

    locr=location.residence
    locp=location.project
    locpm=location.projectmanager  
    loch=location.hardware
    loct=location.technology
    locc=location.contract
    d1={'locr':locr,'locp':locp,'locpm':locpm,'loch':loch,'loct':loct,'locc':locc, }
    d2=d
    d1.update(d2)
    
    return json.dumps(d1); '''



'''

@bp.route('/insert')
def insert():
    return render_template('insert.html')



'''



s=requests.Session()
username='ahoehne'
password='Katze7436!'
s.auth=(username,password)
c=s.get('https://intern.inode.at/backoffice/contract/contract_config_edit.php4?Contract_ID=1463383')
s.cookies=c.cookies
print(c.status_code)
print('global session cookie')
print(c.cookies)
method_requests_mapping = {
    'GET': s.get,
    'HEAD': s.head,
    'POST': s.post,
    'PUT': s.put,
    'DELETE': s.delete,
    'PATCH': s.patch,
    'OPTIONS': s.options,
}

@bp.route('/<path:url>', methods=['GET', 'POST'])
def root(url):
    #LOG.info("Root route, path: %s", url)
    # If referred from a proxy request, then redirect to a URL with the proxy prefix.
    # This allows server-relative and protocol-relative URLs to work.
    proxy_ref = proxy_ref_info(request)
    if proxy_ref:
        redirect_url = "/p/%s/%s%s" % (proxy_ref[0], url, ("?" + str(request.query_string) if request.query_string else ""))
        #LOG.info("Redirecting referred URL to: %s", redirect_url)

        return redirect(redirect_url)
    # Otherwise, default behavior
    return render_template('index.html', name=url,request=request)



@bp.route('/<path:url>', methods=method_requests_mapping.keys())
def proxy(url):
    print('function session cookie')
    print(c.cookies)
    

    url='https://intern.inode.at/'+url
   # requests.utils.add_dict_to_cookiejar(s.cookies,c.cookies)
    cookies=dict(test='Feuer')
    requests_function = method_requests_mapping[flask.request.method]
    request = requests_function(url, stream=True, params=flask.request.args,allow_redirects=False, cookies=cookies)
    
    response = flask.Response(flask.stream_with_context(request.iter_content()),
                              content_type=request.headers['content-type'],
                              
                              status=request.status_code, )
    print('request session cookie')
    print(request.cookies)
    
    
    
    return response





    


   

proxy.counter= 0
    



s=requests.Session()
username='ahoehne'
password='Katze7436!'
s.auth=(username,password)
c=s.get('https://intern.inode.at/backoffice/contract/contract_config_edit.php4?Contract_ID=1463383')
s.cookies=c.cookies
print(c.status_code)
print('global session cookie')
print(c.cookies)
method_requests_mapping = {
    'GET': s.get,
    'HEAD': s.head,
    'POST': s.post,
    'PUT': s.put,
    'DELETE': s.delete,
    'PATCH': s.patch,
    'OPTIONS': s.options,
}



@bp.route('/<path:url>', methods=method_requests_mapping.keys())
def proxy(url):
    print('function session cookie')
    print(c.cookies)
    

    url='https://intern.inode.at/'+url
   # requests.utils.add_dict_to_cookiejar(s.cookies,c.cookies)
    cookies=dict(test='Feuer')
    requests_function = method_requests_mapping[flask.request.method]
    request = requests_function(url, stream=True, params=flask.request.args,allow_redirects=True, cookies=cookies)
    
    response = flask.Response(flask.stream_with_context(request.iter_content()),
                              content_type=request.headers['content-type'],
                              
                              status=request.status_code, )
    print('request session cookie')
    print(request.cookies)
    
    
    
    return response





    


   

proxy.counter= 0
   


