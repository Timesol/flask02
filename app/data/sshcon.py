

from pexpect import pxssh
import getpass
try:
    s = pxssh.pxssh()
    hostname = input('hostname: ')
    username = input('username: ')
    password = getpass.getpass('password: ')
    s.login(hostname, username, password)
    s.sendline('eval "{ sleep 1; echo ahoehne; sleep 1; echo net7toor; sleep 1; echo 'ls'; sleep 5; }" | telnet 192.168.0.136')   
    s.prompt()             
    print(s.before)        
   
    
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)




eval "{ sleep 1; echo ahoehne; sleep 1; echo net7toor; sleep 1; echo 'ls'; sleep 5; }" | telnet 192.168.0.136
 
