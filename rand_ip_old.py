# Generates a random, vaild ip address on a subnet. works for both ipv4|6
import ipaddress
import random

originalip = "190.192.192.192/8"

network = ipaddress.ip_network(originalip, strict=False)

if "/" not in originalip:
    newip = originalip
else:
    maxhosts = ipaddress.ip_network(originalip, strict=False).num_addresses - 2
    newip = network[random.randint(1, maxhosts)]

print(newip)
