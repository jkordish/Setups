title: OpenBSD DHCPD with Dynamic DNS
date: 2012-09-25

[Walkthrough](https://github.com/joethemongoose/Setups/tree/master/DHCP-DDNS)

Relatively simple setup to enable a local DHCP server with dynamic DNS updates for a lab domain.

# Tested and implemented on OpenBSD 5.1.

###

bash-4.2# uname -a

    OpenBSD puffy 5.1 GENERIC#160 i386

bash-4.2# cat /etc/myname
    
    puffy.lab.ttc
    
###

# Instructions

The shipped DHCPD server does not support ddns so we must install the ISC-DHCPD one.

    bash-4.2# pkg_add -r ftp://mirror.esc7.net/pub/OpenBSD/5.1/packages/i386/isc-dhcp-server-4.2.3.2.tgz

You can verify that you installed it.

    bash-4.2# pkg_info -a

    isc-dhcp-server-4.2.3.2 ISC DHCP Server

Create some additional NAMED files for logs.
    
    bash-4.2# touch /var/named/named.run

    bash-4.2# touch /var/named/named_query.log

    bash-4.2# touch /var/named/named_dump.db

    bash-4.2# chown named:named /var/named/named.run

    bash-4.2# chown named:named /var/named/named_query.log

    bash-4.2# chown named:named /var/named/named_dump.db

You will want to change the permission since we are running as user NAMED.

    bash-4.2# chown named:named /var/named/master

    bash-4.2# chgrp named /var/named/etc

    bash-4.2# chown named:named /var/named/etc/*


Ensure your permissions for /var/named/ are correct. The following are what mine look like.
###### you may not have some of the db. files just yet.

    bash-4.2# ls -l /var/named/

        drwxr-xr-x  2 root   wheel      512 Jul 12 07:21 dev

        drwxr-x---  2 root   named      512 Jul 11 10:59 etc

        drwxrwxr-x  2 named  named      512 Jul 13 06:26 master

        -rw-rw-r--  1 named  named  4564137 Jul 13 07:52 named.run

        -rw-rw-r--  1 named  named        0 Jul 12 07:31 named_dump.db

        -rw-rw-r--  1 named  named        0 Jul 12 07:31 named_query.log

        drwxrwxr-x  2 root   named      512 Feb 12 10:32 slave

        drwxr-xr-x  2 root   wheel      512 Jul 11 10:28 standard

        drwxrwxr-x  2 root   named      512 Feb 12 10:32 tmp

    bash-4.2# ls -l /var/named/etc/

        -rw-r-----  1 named  named  1549 Jul 12 13:51 named.conf

        -rw-r-----  1 named  named    77 Jul 11 10:59 rndc.key

        -rw-r--r--  1 named  named  3110 Feb 12 10:32 root.hint

    bash-4.2# ls -l /var/named/etc/master/

        -rw-r--r--  1 named  named   794 Jul 13 06:26 db.10.120.10

        -rw-r--r--  1 named  named  1478 Jul 13 06:26 db.lab.ttc
    
Edit your /etc/dhcpd.conf file. Use the one I've provided for reference/template.

Edit your /var/named/named.conf file. Use the one I've provided for reference/template.

Change the daemon in /etc/rc.d/dhcpd to point to /usr/local/sbin/dhcpd
###### I think this isn't the right way to do it since it may not stay during updates to the base os.

    bash-4.2# sed -i 's/\/usr\/sbin\/dhcpd/\/usr\/local\/sbin\/dhcpd/' /etc/rc.d/dhcpd

Add both DHCPD and NAMED to your /etc/rc.conf.local file for startup.

    bash-4.2# echo 'dhcpd_flags=""' >> /etc/rc.conf.local

    bash-4.2# echo 'named_flags="-u named -d 3"' >> /etc/rc.conf.local

Now start both daemons. Hopefully they start...

    bash-4.2# /etc/rc.d/dhcpd start

    bash-4.2# /etc/rc.d/named start


## Addendum
I've noticed two machines in my lab that never got a ddns record set during DHCP addressing.
Apparently not all systems play nice with DHCP and don't send their
hostname when they communicate with the server. You can manually force
this on a linux machine.

    Fedora 11: 
    echo 'send host-name "fred";' >> /etc/dhclient-eth0.conf
    Ubuntu 10.04: 
    echo 'send host-name "barney";' >> /etc/dhcp3/dhclient.conf

Depending on distrobution and version you may have to look in different
locations.

There may be cases were you are unable to send the hostname. You may
force it within the dhcpd.conf file itself. Look at the dhcpd.conf file
included for an example.

Questions/Comments/Priases can be sent to me at <joe@unicornclouds.com>
