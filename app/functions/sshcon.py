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
sshServer = "192.168.0.192"
jumpcon='telnet 192.168.0.136'
endcon='telnet 62.99.227.25'
aduser='admin'

def connector(sshUsername,sshPassword,endcon ,jumpcon, aduser):

    connection = ssh(sshServer, sshUsername, sshPassword)
    connection.sendCommand("""eval "{{ sleep 1; echo {0}; sleep 1; echo {1}; sleep 1; echo ls; sleep 2; echo {2}; sleep 1; echo {4}; sleep 1; echo {1};
    sleep 1; echo sh run; sleep 5; 
    echo sh ip int br; sleep 1;
    echo show version; sleep 2;
    echo show cellular 0 radio; sleep 2;
    echo wr mem; sleep 2;



    }}" | {3} """.format(sshUsername,sshPassword,endcon ,jumpcon, aduser))








