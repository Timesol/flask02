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
 
                    return str(alldata, "utf8")
        else:
            print("Connection not opened.")


sshUsername = 'ahoehne'
sshPassword = "Katze7436!"
sshServer = "10.146.140.166"
jumpcon='telnet at-vie-xion-pe01'
endcon='telnet vrf 04325363:B2B_ADLER 10.17.1.254'
aduser='ahoehne'

def connector(sshUsername,sshPassword,endcon ,jumpcon, aduser,script):
    #{0}= Username Jumphost 
    #{1}= Password Jumphost 
    #{2}= End Connection ...telnet ...
    #{3}= Jump Connection
    #{4}= Username En Connection
    #{5}= Scriptbody

    connection = ssh(sshServer, sshUsername, sshPassword)
    test=connection.sendCommand("""eval "{{ sleep 1; echo {0}; sleep 1; echo {1}; sleep 2; echo {2}; sleep 1; echo {4}; sleep 1; echo {1};
    
    {5}


    }}" | {3} """.format(sshUsername,sshPassword,endcon ,jumpcon, aduser,script))

    

    return test










