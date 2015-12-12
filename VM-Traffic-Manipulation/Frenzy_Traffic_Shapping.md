title: Frenzy Virtual Traffic Shapping
date: 2012-09-25

[Walkthrough](https://github.com/joethemongoose/Setups/tree/master/VM-Traffic-Manipulation)

Hopefully this will be a relatively simple setup on configuring a transparent bridge to perform traffic shaping & manipulation.
This will allow you to inject artificial latency, bandwidth limits, and packet loss across multiple VirtualMachines for testing.

### Obtain Frenzy.
This uses the bootable FreeBSD distrobution called Frenzy. The latest, as of writing, is 1.4 which is based off of FreeBSD 8.3 Stable.

        http://frenzy.org.ua/en/index.shtml

        wget ftp://ftp.frenzy.org.ua/pub/Frenzy/1.4/iso/frenzy-1.4-lite-en.iso

You will of course now need to get that into your shared storage within vCenter.

### Setup virtual networking
You will want to create two virtual standard switches on your ESXi server. One vSwitch will have no uplinks and the other will have one.
        We will call these two vSwitches vss_Isolated and vss_Lab
Add/Change all the network adapters for all the virtual machines that you want to manipulate to the vSwitch that has NO uplink.
        Should have been called vss_Isolated
        
        note: You can see a screenshot of how I have set it up within this repo.
        
### Create Frenzy Virtual Machine
Create a small virtual machine with roughly 256M of memory and no hard disk.
Create two network adapters. Attach the first adapter to vss_Isolated and next adapater to vss_Lab.
Attach the Frenzy iso to the cdrom and ensure it connects at boot up.
Power on the newly created Frenzy Virtual Machine.

### Configure Frenzy for traffic manipulation
Once Frenzy finshes booting up it will drop you right to a root prompt.

        note: em0 should be vss_Isolated and em1 should be vss_Lab
          
#### create bridge
        ifconfig bridge create
        ifconfig bridge0 addm em0 addm em1 up
        ifconfig em0 up
        ifconfig em1 up

#### make bridge go through ipfw
        sysctl net.link.bridge.ipfw=1

#### Flush the running firewall rules
        ipfw flush

#### create your pipes
        ipfw add pipe 1 ip from any to any via em0
        ipfw add pipe 2 ip from any to any via em1
        ipfw pipe 1 config bw 640Kbit/s queue 30 delay 64ms plr .01
        ipfw pipe 2 config bw 128Kbit/s queue 10 delay 64ms plr .01
        ipfw list
        
That will create one pipe (1) for outgoing traffic and another (2) for incoming traffic with a bad ADSL bandwidth allocation (bw).
It will also add 64ms of latency (delay) and a small packet loss (plr)

#### Optional: Allocate more memory
Dummynet can end up using a lot of memory based off of how much it is being taxed. Allocate 32MB worth of memory to network mbufs.
        sysctl kern.ipc.nmbclusters=32768

### Done
That should be it. You can check by pinging the gateway. You can also test by doing a speedtest. I like http://speedof.me since it uses HTML5.
I have added a screenshot of my final speedtest showing this.

Questions/Comments/Priases can be sent to me at <joe@unicornclouds.com>
