#!/usr/bin/env python

import nmap
import time
nm = nmap.PortScanner()


print('----------------------------------------------------')
time.sleep(1)

def sweep():
	nm.scan(hosts='10.0.0.8', arguments='-n -sP -PE -PA21,23,80,3389')
	hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
	for host, status in hosts_list:
	    print('{0}:{1}'.format(host, status))
for i in range(5):
	sweep()
	time.sleep(30)
