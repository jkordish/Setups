title: Nova Compute Bug 1081808 Fix
date: 2013-01-25

I recently ran into an odd bug in nova-compute where the service would crash any time the server reboot or the nova-compute service restarted. Turns out this is a known [bug](https://bugs.launchpad.net/nova/+bug/1081808) and will be fixed in grizzly.

Since it took me a while to figure this out I wanted to write up how to resolve this in hopes it will cut down others time in resolving this issue.

I honestly wish I could explain why all of the sudden this appeared and wasn't affecting be prior. Who cares this solves it!


### Bug

You will notice that the nova-compute will crash.

    # nova-manage service list
    nova-compute        HOST       nova    enabled XXX     DATE TIME

Investigating /var/log/nova/nova-compute.log you'll notice something very similar to the following.


    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/nova/service.py", line 398, in start
    2013-01-25 06:53:40 20841 TRACE nova     self.manager.init_host()
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/nova/compute/manager.py", line 314, in init_host
    2013-01-25 06:53:40 20841 TRACE nova     block_device_info)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/nova/exception.py", line 117, in wrapped
    2013-01-25 06:53:40 20841 TRACE nova     temp_level, payload)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/contextlib.py", line 24, in __exit__
    2013-01-25 06:53:40 20841 TRACE nova     self.gen.next()
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/nova/exception.py", line 92, in wrapped
    2013-01-25 06:53:40 20841 TRACE nova     return f(*args, **kw)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/nova/virt/libvirt/driver.py", line 1013, in resume_state_on_host_boot
    2013-01-25 06:53:40 20841 TRACE nova     block_device_info)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/nova/virt/libvirt/driver.py", line 1931, in _create_domain_and_network
    2013-01-25 06:53:40 20841 TRACE nova     domain = self._create_domain(xml)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/nova/virt/libvirt/driver.py", line 1910, in _create_domain
    2013-01-25 06:53:40 20841 TRACE nova     domain.createWithFlags(launch_flags)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/eventlet/tpool.py", line 187, in doit
    2013-01-25 06:53:40 20841 TRACE nova     result = proxy_call(self._autowrap, f, *args, **kwargs)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/eventlet/tpool.py", line 147, in proxy_call
    2013-01-25 06:53:40 20841 TRACE nova     rv = execute(f,*args,**kwargs)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/eventlet/tpool.py", line 76, in tworker
    2013-01-25 06:53:40 20841 TRACE nova     rv = meth(*args,**kwargs)
    2013-01-25 06:53:40 20841 TRACE nova   File "/usr/lib/python2.7/dist-packages/libvirt.py", line 650, in createWithFlags
    2013-01-25 06:53:40 20841 TRACE nova     if ret == -1: raise libvirtError ('virDomainCreateWithFlags() failed', dom=self)
    2013-01-25 06:53:40 20841 TRACE nova libvirtError: Requested operation is not valid: domain is already running
    2013-01-25 06:53:40 20841 TRACE nova

Pay attention to the *libvirtError*

### Manually

Add the following two lines into /etc/nova/nova.conf

    # vim /etc/nova/nova.config

    start_guests_on_host_boot=false
    resume_guests_state_on_host_boot=true

Restart the services

    # service nova-compute restart

### RCBOPS

There is a easier way to resolve this if you happen to utilize the [RCBOPS-Cookbooks](https://github.com/rcbops-cookbooks/).

**UPDATED: 4 Feb 2013** Someone emailed me on my previous lines not working. I've resolved the issues and updated the knife exec syntax.

    $ sudo -i

    # knife exec -E '@e=Chef::Environment.load("rpcs"); \
    a=@e.override_attributes; \
    a["nova"].merge!({"config" => {"start_guests_on_host_boot" => false, "resume_guests_state_on_host_boot" => true}}); \
    @e.override_attributes(a); @e.save'

    # chef-client

    # service nova-compute restart

### Done
Hope that helps.

Questions/Comments/Priases can be sent to me at <joe@unicornclouds.com>
