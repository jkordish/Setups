#!/usr/bin/env python

import sys
import os
import etcd

if len(sys.argv) == 1:
    sys.stderr.write('Usage: %s --list|--host host\n' % (sys.argv[0]))
    sys.exit(1)

c = etcd.Client()

id = os.getenv('ANSIBLE_ID')

if sys.argv[1] == "--list":
    hosts = c.read('customers/%s/hosts' % (id), recursive = True, sorted = True)
    list = []
    for child in hosts.children:
        list.append(str(child.key))
    print c.get(sorted(list, reverse=True)[0]).value
