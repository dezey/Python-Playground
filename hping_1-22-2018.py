###################################################################
""" get various information to uniquely identify packets,
    need to include 'real source ip',  """
###################################################################

"""get date in yyyy-mm-dd HH:MM:SS format """
import datetime
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(now)

###################################################################
""" for-loop attempt """
###################################################################
""" import things """
import ipaddress
import random
import glob
import xml.etree.ElementTree as ET
import ipaddress
import random
import socket   
import subprocess
import hashlib

from scapy.all import *

"""Generates a random, vaild ip address on a subnet. works for both ipv4|6.
   if no cdir/mask given instead just feeds the original back."""
def ipgen(originalip):
    if "/" not in originalip:
        return originalip
    else:
        network = ipaddress.ip_network(originalip, strict=False)
        """ the minus 1 (one) below is to translate the maxhosts value 
            to a list index value otherwise the upper limit of the 
            network range would be outside of the network[n-n] range"""
        maxhosts = ipaddress.ip_network(originalip, strict=False).num_addresses - 1
        newip = network[random.randint(0, maxhosts)]
        return newip

path = '*.xml'
files = glob.glob(path)

""" coutner for number on rules related to a specfic action """
totalreject = 0
totalaccept = 0
totaldrop = 0

for xmlfile in files:
    
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    for child in root:
        for grandchild in child:
            if grandchild.tag == "reject":
                totalreject += 1
            if grandchild.tag == "accept":
                totalaccept += 1
            if grandchild.tag == "drop":
                totaldrop += 1
                
totalrules = totalreject + totalaccept + totaldrop
#print("the total number of rules is " + str(totalrules))
#print("total number of reject rules is " + str(totalreject))
#print("total number of accept rules is " + str(totalaccept))
#print("total number of drop rules is " + str(totaldrop))
print(" ")
""" Gathering rule specfic information and generating a packet that fits the rule"""

""" some varibles """
sourceaddr = ""
sourceactual = ""
destinationaddr = ""
portnum = ""
protocol = ""
myip = socket.gethostbyname(socket.getfqdn())
agents = ['192.168.1.152', '172.11.11.55']
action = ""     

for xmlfile in files:
    
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    for child in root:
        if child.tag == 'rule':
            sourceaddr = child.find('source').attrib['address']
            destinationaddr = child.find('destination').attrib['address']
            portnum = child.find('port').attrib['port']
            protocol = child.find('port').attrib['protocol']
                    
            for grandchild in child:
                if grandchild.tag == "reject":
                    action = "reject"
                if grandchild.tag == "accept":
                    action = "accept"
                if grandchild.tag == "drop":
                    action = "drop" 
            
            print(sourceaddr + ", " + destinationaddr + ", " + portnum + ", " + protocol + ", " + action)
            
            """ Creates non-masqueraded packets based on machines ip"""
            if ipaddress.ip_address(myip) in ipaddress.ip_network(sourceaddr, strict=False):
                for IP in agents:
                    if ipaddress.ip_address(IP) in ipaddress.ip_network(destinationaddr, strict=False) and IP != myip:
                        print("Crafting non-masq packet: " + myip + ", " + IP + ", " + portnum + ", " + protocol + ", " + action)
                        
                        tobehash = myip + IP + portnum + protocol + action
                        hashed = hashlib.sha512(tobehash.encode()).hexdigest()
                        
                        file = open('hold.txt','w') 
                        file.write(hashed) 
                        file.close() 
                        
                        file = open('hold.txt','r')
                        print(file.read())
                        file.close()
                        
                        count = 3
                        subprocess.run(["ping","-n ", str(count), IP])
                        
            """ creates masqueraded packets for everything (creates a masquerade for the non-masqueraded as well)"""           
            for IP in agents:
                if ipaddress.ip_address(IP) in ipaddress.ip_network(destinationaddr, strict=False):
                    newsrcip = str(ipgen(sourceaddr))
                    print("Crafting masq packet: " + newsrcip + ", " + IP + ", " + portnum + ", " + protocol + ", " + action)
                    
                    tobehash = newsrcip + IP + portnum + protocol + action
                    hashed = hashlib.sha512(tobehash.encode()).hexdigest()
                        
                    file = open('hold.txt','w') 
                    file.write(hashed) 
                    file.close()
                    
                    file = open('hold.txt','r')
                    print(file.read())
                    file.close()
                    
            print(" ")      
            
