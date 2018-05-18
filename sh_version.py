import argparse
import getpass
from netmiko import ConnectHandler

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--username", help="Login Username",
                        action="store")
    parser.add_argument('-p', "--password", help="Login password",
                        action="store")
    parser.add_argument('-f', "--in_host", help="Input the host name",
                        action="store")
    args = parser.parse_args()

    if not args.username:
        args.username = raw_input("Login Username: ")
    if not args.password:
        args.password = getpass.getpass("Login Password: ")
    if not args.in_host:
        args.in_host = raw_input("Enter device name: ")

    return (args.username,args.password,args.in_host)



def login(username, password, device):
    '''
    Logs in to the ios device; change device_type to 'cisco_nxos' if device is nexus. Refer netmiko git link above
    :return:
    '''
    session = ConnectHandler(device_type='cisco_nxos',
                                  ip=device,
                                  username=username,
                                  password=password)

    return session

def run(session):
        '''
        Runs show runn command and returns output as list
        '''

        output = session.send_command('show ver')
        output = output.split('\n')


        return output


def logout(session):
    '''
    logs out of device
    '''
    session.disconnect()


    return True

def writer(output,ip):
    '''
    Write the show run outputs to a text file
    '''

    file_name = '{}.txt'.format(ip)

    with open(file_name,'w') as the_file:
        for line in output:
            the_file.write(line + '\n')


    return True


#main

(username, password, device) = arguments()
session = login(username, password, device)
output = run(session)
logout(session)
writer(output,device)
