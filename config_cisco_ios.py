from netmiko import Netmiko
from multiprocessing.dummy import Pool as ThreadPool
import time

f_2 = open("multiple_device_list_cisco.txt","r")
multiple_device_list = f_2.readlines()

f_3 = open("Syslog_Unsuccess_Connection.txt","a")

with open("user_pass.txt", "r") as f5:
    user_pass = f5.readlines()

for list_user_pass in user_pass:
    if "username" in list_user_pass:
        username = list_user_pass.split(":")[1].strip()
    if "password" in list_user_pass:
        password = list_user_pass.split(":")[1].strip()

file1 = open("Syslog_Cisco_OK.txt", "a")

def _ssh_(nodeip):

    try:
        cisco = {
            'device_type': 'cisco_ios', 'ip': nodeip, 'username':
            username, 'password': password, 'secret':password, "conn_timeout": 20}
        cisco_connect = Netmiko(**cisco)
        print(nodeip.strip() + "  " + "is reachable")
    except Exception as e:
        print (e)
        f_3.write(nodeip.strip() + "\n")
        return

    prompt_cisco_fnk = cisco_connect.find_prompt()
    hostname_fnk = prompt_cisco_fnk.strip("#")
    print(hostname_fnk)
    cisco_connect.send_command_timing("configure terminal")
    print("entered config mode")
    cisco_connect.send_command_timing("logging 192.168.0.X")
    cisco_connect.send_command_timing("exit")

    data_to_parse = cisco_connect.send_command_timing('show run | i 192.168.0.X')
    output = ''.join(data_to_parse)
    output2 = output.splitlines()
    output3 = ''.join(output2)
    output4 = output3.split(" ")
    if "10.222.246.12" in output4:
        print("config done")
        file1.write(nodeip + "\n")
    else:
        print(nodeip + "config:nok")

    cisco_connect.send_command_timing("write")
    cisco_connect.disconnect()

myPool = ThreadPool(100)
result = myPool.map(_ssh_,multiple_device_list)


