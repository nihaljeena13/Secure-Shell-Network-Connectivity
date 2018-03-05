#!/usr/bin/env python


#necessary modules to be used.
import paramiko
import threading
import os.path
import subprocess
import time
import sys
import re


#Checking IP address file and content validity
def ip_is_valid():
    check = False
    global ip_list
    
    while True:


        #Prompting user for input

        ip_file = raw_input(" Enter IP file name and extension: ")

        # If user enters the correct filename it will execute the try block that is opening the file and storing its contents in a global variable ip_list.
        # else executes an except block.
        try:
            #Open user selected file for reading (IP addresses file)
            selected_ip_file = open(ip_file, 'r')
            
            #Starting from the beginning of the file
            selected_ip_file.seek(0)
            
            #Reading each line (IP address) in the file
            ip_list = selected_ip_file.readlines()
            
            #Closing the file
            selected_ip_file.close()
            
        except IOError:
            print "\n The file %s you entered does not exist.\n" % ip_file
            
        #Checking each ip address in a file if its valid or not
        for ip in ip_list:
            a = ip.split('.')
            
            if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
                check = True
                break
                 
            else:
                print '\n There is an invalid ip adress . Please checl the ip file.\n'
                check = False
                continue
            
        #Evaluating the check flag
        if check == False:
            continue
        
        elif check == True:
            break


    
    #Checking IP reachability.

     check2 = False
    
    while True:
        for ip in ip_list:

            #giving command to linux shell using python subprocess module and pinging each ip to check its reachability.
            ping_reply = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', ip])

            #if ping_reply == 0, then continue pinging next IP.
            if ping_reply == 0:
                check2 = True
                continue
            
            elif ping_reply == 2:
                print "\n No response from the device %s." % ip
                check2 = False
                break
            
            else:
                print "\n Pinging has failed for the followig device:", ip
                check2 = False
                break
            
        #Evaluating the check flag
        if check2 == False:
            print " Please recheck IP address list in ip file or the device.\n"
            ip_is_valid()

        
        elif check2 == True:
            print '\n All devices are reachable.\n'
            break

#Checking user file validity
#This file contains the special credentials i.e. username and password.
def user_is_valid():
    global user_file
    
    while True:

        user_file = raw_input(" Enter user/password file name and extension: ")

        
        #To check the file if it is present on your OS using isfile() function with os.path module.
        if os.path.isfile(user_file) == True:
            print "\n Username/password file has been validated. \n"
            break
        
        else:
            print "\n The file %s you entered does not exist.\n" % user_file
            continue

#Checking command file validity
#This file contain the commands to send to routers.
def cmd_is_valid():
    global cmd_file
    
    while True:

        cmd_file = raw_input(" Enter command file name and extension: ")

        
        #to check the file if it is present on your OS using isfile() function with os.path module.
        if os.path.isfile(cmd_file) == True:
            print "\n Sending command(s) to device(s)...\n"
            break
        
        else:
            print "\n The file %s you entered does not exist.\n" % cmd_file
            continue

#call these functions using try and catch block as the user might want to interrupt the execution using CTRL + C
try:
    #Calling IP validity function    
    ip_is_valid()
    
except KeyboardInterrupt:
    print "\n Program aborted by user. Exiting...\n"
    sys.exit()


try:
    #Calling user file validity function    
    user_is_valid()
    
except KeyboardInterrupt:
    print "\n Program aborted by user. Exiting...\n"
    sys.exit()
    

try:
    #Calling command file validity function
    cmd_is_valid()
    
except KeyboardInterrupt:
    print "\n Program aborted by user. Exiting...\n"
    sys.exit()




#Open SSHv2 connection to devices
def open_ssh_conn(ip):

    try:
        #Opening user_file to collect the SSH parameters.
        selected_user_file = open(user_file, 'r')
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #Reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0]
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #Reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        
        #Logging into device
        session = paramiko.SSHClient()
        
        #For testing purposes, this allows auto-accepting unknown host keys using the AutoAddPolicy() method
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #Connect to the device using username and password          

        session.connect(ip, username = username, password = password)
        
        #Start an interactive shell session on the router
        connection = session.invoke_shell()	
        
        #The first command to send in a shell is the terminal length command to capture the longest output from the router.
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        #Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')
            
        #Starting from the beginning of the file
        selected_cmd_file.seek(0)
        
        #Writing each line in the file to the device, i.e. sending commands to the devices from the file
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        
        #Closing the user file
        selected_user_file.close()
        
        #Closing the command file
        selected_cmd_file.close()
        
        #output from commands stored in router_output to check the IOS syntax errors.
        router_output = connection.recv(65535)

        #using regexp to search for the IOS syntax errors.
        if re.search(r"% Invalid input detected at", router_output):
            print " There was at least one IOS syntax error on device %s" % ip
            
        else:
            print "\nDONE for device %s" % ip
            
        #Test for reading command output
        #print router_output + "\n"
        
        #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print " Invalid username or password. \n Please check the username/password file or the device configuration!"


#Creating threads to send configuration commands to the routers simultaneously using threading module.
def create_threads():
    threads = []
    for ip in ip_list:
        th = threading.Thread(target = open_ssh_conn, args = (ip,))   #args is a tuple with a single element
                                                                      #function targeted is open_ssh_conn
        th.start()
        threads.append(th)
        
    for th in threads:
        th.join()

#Calling threads creation function
create_threads()

#End of program