###################################################################
"""Generates a random, vaild ip address on a subnet. works for both ipv4|6.
 if no cdir/mask given instead just feeds the original back."""
 ###################################################################+++++++++++++++++++++++++++++++++++++++++

"""
import ipaddress
import random

originalip = "192.168.0.0/31"

def ipgen(originalip):
    if "/" not in originalip:
        return originalip
    else:
        network = ipaddress.ip_network(originalip, strict=False)
        """ """ the minus 1 (one) below is to translate the maxhosts value 
            to a list index value otherwise the upper limit of the 
            network range would be outside of the network[n-n] range""" """
        maxhosts = ipaddress.ip_network(originalip, strict=False).num_addresses - 1
        newip = network[random.randint(0, maxhosts)]
        return newip


print(ipgen(originalip))
"""

###################################################################
"""get xml data from .xml file (work in progress)
    aka read xml files"""
###################################################################

"""
import xml.etree.ElementTree as ET
rulenumber = 3

xmlfile = 'public2.xml'
local = './rule[' + str(rulenumber)
#sourceip = local + ']/source'
tree = ET.parse(xmlfile)
#sourceip = [el.attrib.get('address') for el in tree.findall(sourceip)]
#action = tree.find('./rule[1]/accept')

action_local = local + ']/' + actions[listplace]
actions = ['accept', 'reject', 'drop']
listplace = 0
action = tree.find(action_local)

while action is None: 
    action_local = local + ']/' + actions[listplace]
    listplace = listplace + 1
    action = tree.find(action_local)
    

print(action.tag)

"""
###################################################################
"""get the number of rules in a .xml. This is so when I make a loop
    I know how many times to loop/when to stop"""
###################################################################
"""
with open(xmlfile) as f:
    total = 0
    for line in f:
        finded = line.find('<rule ')
        if finded != -1 and finded !=0:
            total += 1

print(total)
"""
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

import ipaddress
import random
import glob
import xml.etree.ElementTree as ET
import ipaddress
import random

from xml.dom import minidom

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

""" below is the first attempt, long, overly complex attempt

for xmlfile in files:
    with open(xmlfile) as f:
        #counter for total number of (x) rules
        total = 0
        accepttotal = 0
        rejecttotal = 0
        droptotal = 0
        for line in f:
            #find total number of rules
            totalfound = line.find('<rule ')
            if totalfound != -1 and totalfound !=0:
                total += 1
            #find total number of accept rules
            acceptfound = line.find('<accept/>')
            if acceptfound != -1 and acceptfound !=0:
                accepttotal += 1
            #find total number of reject rules
            rejectfound = line.find('<reject/>')
            if rejectfound != -1 and rejectfound !=0:
                rejecttotal += 1
            #find total number of drop rules
            dropfound = line.find('<drop/>')
            if dropfound != -1 and dropfound !=0:
                droptotal += 1

    rulenumber = 1
    while rulenumber <= total:
        #General varibles
        local = './rule[' + str(rulenumber)
        sourceippath = local + ']/source'
        portpath = local + ']/port'
        protocolpath = local + ']/port'
        tree = ET.parse(xmlfile)
        
        #Grab rule information to generate packet
        sourceip = [el.attrib.get('address') for el in tree.findall(sourceippath)]
        port = [el.attrib.get('port') for el in tree.findall(portpath)]
        protocol = [el.attrib.get('protocol') for el in tree.findall(protocolpath)]
        
        #Varibles needed for determine expected rule action
        actions = ['accept', 'reject', 'drop']
        listplace = 0
        action_local = local + ']/' + actions[listplace] 
        action = tree.find(action_local)

        #actually determine expected rule action
        while action is None: 
            action_local = local + ']/' + actions[listplace]
            listplace = listplace + 1
            action = tree.find(action_local)
        
        print("hping -sourceip " + str(ipgen(sourceip[0])) + " -port " + str(port[0]) + " -protocol " + str(protocol[0]) + " -action " + action.tag)
        rulenumber = rulenumber + 1
"""


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

print("the total number of rules is " + str(totalrules))
print("total number of reject rules is " + str(totalreject))
print("total number of accept rules is " + str(totalaccept))
print("total number of drop rules is " + str(totaldrop))



sourceaddr = ""
sourceactual = ""
destinationaddr = ""
portnum = ""
protocol = ""
action = ""

validdest = ['192.168.1.0/24','168.1.0.0/18']
actualdest = ['192.168.1.150','168.1.0.150']
for xmlfile in files:
    
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    
    """Get the total number of rules in the xml file"""
    xmldoc = minidom.parse(xmlfile)
    itemlist = xmldoc.getElementsByTagName('rule')
    numrules = (len(itemlist))

    """ get the total  number of childs in the xml file"""    
    numchilds = 0
    for child in root:
        numchilds += 1             
    
    start = numchilds - numrules
    print(start)
    for child in root:
        if start <= (numchilds - 1):
            print(root[start].find('source').attrib['address'])
            print(root[start].find('destination').attrib['address'])
            print(root[start].find('port').attrib['port'])
            print(root[start].find('port').attrib['protocol'])
            start += 1
"""
            if grandchild.tag == "source":
                sourceaddr = grandchild.attrib['address']
                sourceactual = ipgen(sourceaddr)
                if grandchild.tag == "destination":
                    destinationaddr = grandchild.attrib['address']
                    if grandchild.tag == "port":
                        portnum = grandchild.attrib['port']
                        protocol = grandchild.attrib['protocol']
                        if grandchild.tag == "reject":
                            action = "reject"
                        if grandchild.tag == "accept":
                            action = "accept"
                        if grandchild.tag == "drop":
                            action = "drop"
                        
                        print(sourceaddr)
                        print(sourceactual)
                        print(destinationaddr)
                        print(portnum)
                        print(protocol)
                        print(action) 
   
"""                    
"""
for child in root:
        test += 1
        #print(root[4][0].attrib['address'])              
        for grandchild in child:
            sourceaddr = child.cc
            destinationaddr = child.find('destination').attrib['address']
            portnum = child.find('port').attrib['port']
            protocol = child.find('port').attrib['protocol']
            if sourceaddr != "None":
                #print(ipgen(sourceaddr))
                #print(destinationaddr)
                #print(portnum)
                #print(protocol)
                pass
"""
"""
    totals = 0
    for child in root:
        if child.tag == "rule":
            totals += 1 
        ruleplacehold = 4
        while ruleplacehold <= (totals + 4):
            print(root[ruleplacehold][0].attrib['address'])                              
            print(root[ruleplacehold][1].attrib['address'])
            print(root[ruleplacehold][2].attrib['protocol'])
            print(root[ruleplacehold][2].attrib['port'])
            print(root[ruleplacehold][3].tag)
    
            ruleplacehold += 1
"""

















