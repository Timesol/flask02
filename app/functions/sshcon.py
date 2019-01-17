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







def connector(endcon ,jumpcon, userjump,passjump,userend,passend,script,sshServer, sshUsername, sshPassword):
    #{2}= Username Jumphost 
    #{3}= Password Jumphost 
    #{0}= End Connection ...telnet ...
    #{1}= Jump Connection
    #{4}= Username End Connection
    #{5}= Password End Connection
    #{6}= Scriptbody

    print('In Connector Function')
    
    connection = ssh(sshServer, sshUsername, sshPassword)
    test=connection.sendCommand("""eval "{{ sleep 1; echo {2}; sleep 1; echo {3}; sleep 1; echo {0}; sleep 1; echo {4}; sleep 1; echo {5}; sleep 3;
    
    echo cat <<EOF; sleep 1; echo {6}; echo EOF;


    }}" | {1} """.format(endcon ,jumpcon, userjump,passjump,userend,passend,script))

    

    return test










