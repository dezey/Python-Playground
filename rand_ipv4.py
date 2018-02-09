# Generates a random, vaild ip address on a subnet. works for both ipv4|6
import ipaddress
import random

originalip = "190.192.192.192"

network = ipaddress.ip_network(originalip, strict=False)

"""below command takes way to much memory"""
#maxhosts = len(list(ipaddress.ip_network(network).hosts()))

"""below was used to calc max hosts but limited func to only cdir"""
#ip_mask = originalip.split("/")[1]
#ip_mask = int(ip_mask)

ver = network.version

maxhosts = ipaddress.ip_network(originalip, strict=False).num_addresses - 2

#if ver == 6:
#    maxhosts = 2 ** (124 - ip_mask) - 2
#else:
#    maxhosts = 2 ** (32 - ip_mask) - 2

newip = network[random.randint(1, maxhosts)]
print(maxhosts)
print(newip)
