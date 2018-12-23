

    
from paramiko import client

class ssh:
    client = None
 
    def __init__(self, address, username, password):
        print("Connecting to server.")
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
 
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


sshUsername = 'ahoehne'
sshPassword = "net7toor"
sshServer = "192.168.0.213"



connection = ssh(sshServer, sshUsername, sshPassword)
connection.sendCommand("""eval "{{ sleep 1; echo {0}; sleep 1; echo {1}; sleep 2; echo telnet 62.99.227.25; sleep 1; echo admin; sleep 1; echo {1};
sleep 1; echo sh run; sleep 5; 
echo sh ip int br; sleep 1;
echo show version; sleep 2;
echo show cellular 0 radio; sleep 2;
echo wr mem; sleep 2;



}}" | telnet 192.168.0.136 """.format(sshUsername,sshPassword))




'''
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





