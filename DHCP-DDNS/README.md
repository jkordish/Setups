bash-4.2# uname -a
OpenBSD puffy 5.1 GENERIC#160 i386
bash-4.2# uptime
 7:53AM  up 1 day, 31 mins, 1 user, load averages: 0.32, 0.26, 0.23
bash-4.2# cat /etc/myname 
puffy.lab.ttc
bash-4.2# pkg_info -a
isc-dhcp-server-4.2.3.2 ISC DHCP Server
bash-4.2# ls -l /var/named/
total 8984
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
total 24
-rw-r-----  1 named  named  1563 Feb 12 10:32 named-dual.conf
-rw-r-----  1 named  named  1351 Feb 12 10:32 named-simple.conf
-rw-r-----  1 named  named  1549 Jul 12 13:51 named.conf
-rw-r-----  1 named  named    77 Jul 11 10:59 rndc.key
-rw-r--r--  1 named  named  3110 Feb 12 10:32 root.hint
bash-4.2# ls -l /var/named/etc/master/
total 44
-rw-r--r--  1 named  named   794 Jul 13 06:26 db.10.120.10
-rw-r--r--  1 named  named  6533 Jul 13 06:13 db.10.120.10.jnl
-rw-r--r--  1 named  named  1478 Jul 13 06:26 db.lab.ttc
-rw-r--r--  1 named  named  8442 Jul 13 06:13 db.lab.ttc.jnl
