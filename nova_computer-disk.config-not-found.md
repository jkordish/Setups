title: Nova-Compute error - disk.config not found
date: 2013-07-15

Just ran into a weird issue with instances not starting up once I got my OpenStack lab upgraded to Grizzly. Issue was with a disk.config file not being found by nova-compute.

### Bug
Investigating /var/log/nova/nova-compute.log you'll notice something very similar to the following.

    2013-07-15 13:38:02.308 ERROR nova.compute.manager [req-c2523ea9-97e9-4b2a-a420-994acd20f36d c1248849bf7b4aa3a2fc50f3cb3209b9 5c570d6be3e04ad68046108439001ae2] [instance: cd3b6ff2-f2ef-4a76-92e9-e3215366bb10] Cannot reboot instance: [Errno 2] No such file or directory: '/var/lib/nova/instances/instance-0000004d/disk.config'

### Resolution
This ended up being a quick fix but had to be ran on each nova-compute node within the cluster.

    # for i in `ls -d /var/lib/nova/instances/instance*`; do touch $i/disk.config; done

Then it was a matter or just hard-rebooting each instance. In my case I ended up having to reset the instance states back to active though.

    # nova reset-state --active cd3b6ff2-f2ef-4a76-92e9-e3215366bb10
    # nova reboot --hard cd3b6ff2-f2ef-4a76-92e9-e3215366bb10

If I had more time I would better investigate the root cause but time is not on my side.

### Done
Hope that helps.

Questions/Comments/Priases can be sent to me at <joe@unicornclouds.com>