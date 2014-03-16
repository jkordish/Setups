#!/usr/bin/env python

import sys
import os
import etcd

c = etcd.Client()

id = os.getenv('ANSIBLE_ID')

hosts = c.read('customers/%s/hosts' % (id), recursive = True, sorted = True)
list = []
for child in hosts.children:
    list.append(str(child.key))
print c.get(sorted(list, reverse=True)[0]).value
