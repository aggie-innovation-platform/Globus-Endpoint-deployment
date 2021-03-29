#!/usr/bin/env python
import sys
import json
all_ipv4_addr = sys.argv[1]
ipaddrs=json.loads(all_ipv4_addr)
for ip in ipaddrs:
    if "127.0.0" in ip:
        ipparts=ip.split(".")
ipparts[2]=int(ipparts[2])-7
print(json.dumps({"ip":"{}.{}.{}.{}".format(ipparts[0],ipparts[1],ipparts[2],ipparts[3])}))
