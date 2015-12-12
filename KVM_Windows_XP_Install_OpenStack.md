title: Windows XP install guide for KVM and OpenStack
date: 2013-01-31

This is a short reference guide for install Windows XP into a KVM virtual machine. It also outlines how to upload the finished image into Glance to be used by OpenStack.

# Prerequisite

In order to install the Windows XP Operating System you will require the following:

1. KVM is already up and running properly.
2. You have a copy of the Windows XP iso
        $ sudo dd if=/dev/cdrom of=Windows_XP_SP3.iso
3. You have the Windows XP Product License avaiable

## Create Windows XP Hard Drive

You will first be required to create a target hard drive to install Windows on.

        $ cd ~ && mkdir KVM && cd KVM

        $ qemu-img create -f qcow2 winxpsp3.qcow2 10G

**Note:** It is recommended that the hard drive for a Windows XP machine be at least 8G

## Attach ISO and boot

Next we will attach the Windows XP ISO and boot

        $ kvm -m 1024 -cdrom Windows_XP_SP3.iso -boot d winxpsp3.qcow2

## Install Windows

Next you will follow the Windows guided install. You will be required to input a product key during installation. Installation takes roughly 30 minutes.

## Install Virtio Drivers

The [Virtio](http://wiki.libvirt.org/page/Virtio) drivers are require to achieve maximize performance through paravirtualization. In essence the virtual machine understands it is a virtual machine and takes advantage of the underlining hardware.

1. Downloaded the latest [Virtio ISO](http://alt.fedoraproject.org/pub/alt/virtio-win/latest/images/bin/)

**Note:** This ISO is updated on a regular basis. always ensure you have the latest.

1. Attach and boot the Windows XP virtual machine from the previous steps.
        $ qemu-kvm -hda winxpsp3.qcow2 \
            -drive file=winxpsp3.qcow2,if=virtio \
            -drive file=virtio-win-0.1-52.iso,media=cdrom,index=1 \
            -net nic,model=virtio \
            -net user \
            -boot d \
            -vga std \
            -m 1024

1. Once the virtual machine is running, you can cancel every instance of Windows informing you on new hardware.
### SCSI Device Driver
1. Go to *Device Manager*
1. You will notice an section titled *Other devices*
1. Expand *Other devices* and you should see a device for SCSI, Ethernet and VGA
1. Right click the SCSI Controller* device and select *Update driver...*
1. At the *Hardware Update Wizard* click *No, not this time* and click *Next*
1. At the next window, click *Install from list or specific location [Advanced]* and click *Next >*
1. At the *Please choose your search and installation options.* window select *Don't search. I will the driver to install* and click *Next*
1. At the *Hardware Type* window click *Next*
1. At the *Select the device driver you want to install for this hardware.* click *Have Disk...*
1. At the *Install From Disk* window click *Browse...*
1. Navigate to the CDROM and drill down to *wxp\\x86\\* directory and select *VIOSTOR* and click *Open*
1. Windows will attempt to load the drivers and prompt a warning. Click *Continue Anyway*
- If you just do the automatic method it will install the wrong driver which won't initialize and give you an *code: 39* error
### Network Driver
1. Back under *Other devices* right click *Ethernet Controller* and select *Update driver...*
1. At the *Hardware Update Wizard* select *No, not at this time* and click *Next >*
1. At the next window, click *Install from list or specific location [Advanced]* and click *Next >*
1. At the *Please choose your search and installation options* windows ensure *Search for the best driver in these locations* is enabled and click *Next >*
1. Windows should find the correct device driver and prompt you with a warning. Click *Continue Anyway*
1. Once completed, click *Finish*
### VGA Driver
1. Since we will be running this in the OpenStack environment we can safely leave this as is.
## Shutdown
1. Once complete shutdown the virtual machine.
1. You can now relaunch the Windows XP machine
        $ kvm -m 1024 -boot d winxpsp3.qcow2

## Enable Remote Desktop

You will want to enable *Remote Desktop*

1. Right click on *My Computer* and select *Properties*
        Start => My Computer
1. Click on the tab titled *Remote*
1. Enable Remote Desktop by clicking the box *Allow users to connect remotely to this computer*
1. Click *OK*

## Importing into Glance

The following steps outline how you would import the previously created Windows XP image into Glace to be used as a instance type within OpenStack

### Upload into Glance
You can also import this completed virtual machine into Glance so that it may be used for instance deployment within OpenStack

**Note:** The following is done with the assumption that you used the [RackSpace Private Cloud](http://www.rackspace.com/cloud/private/) distribution and AlamoController is the controller.

* If another method was used then you will have to download the 'OpenStack RC File' which can be obtain from Horizon e.g. https://Horizon/settings/project/

1. Copy the image over to AlamoController
        $ scp  winxpsp3.qcow2 admin@AlamoController:~
**Note:** you will have to enter the admin credentials
1. Log in to AlamoController
        $ ssh admin@AlamoController
**Note:** you will have to enter the admin credentials
1. Change to root
        $ sudo -i
1. Load the OpenStack credentials
        # source openrc
1. Navigate back to the admin home directory
        # cd ~admin
1. Upload image into Glance
        # glance image-create --name="Windows XP SP3" --is-public=true --container-format=ovf --disk-format=qcow2 < winxpsp3.qcow2

## OpenStack Instances

The following instructions should outline how you would go about deploying this Windows XP image as an operational instance within OpenStack

### Create Remote Desktop Security Group

You will want to create a Security Group for the remote desktop port

**Note:** The following is done with the assumption that you used the [RackSpace Private Cloud](http://www.rackspace.com/cloud/private/) distro and AlamoController is the controller.

1. Navigate to Horizon
        http://AlamoController
        This probably will be the AlamoController
1. Log in with the credentials previously provided
1. Click *Access & Security* on the left hand side
1. Under *Create Security Group* click *Create Security Group*
1. At the *Create Security Group* window input the following
        Name: Windows
        Description: Remote Desktop Port
1. Click *Create Security Group*
1. Navigate back to *Security Groups* and find the *Windows* Security Group that you just created
1. Click *Edit Rules*
1. At the *Edit Security Group Rules* window input the following
        IP Protocol: TCP
        From Port: 3389
        To Port: 3389
        Source Group: CIDR
        CIDR: 0.0.0.0/00
1. Click *Add Rule*
        You could limit the CIDR to a safe network which prevents random access. 0.0.0.0/0 opens it up for EVERYONE

### Launch Windows XP Instance

The uploaded Windows XP image from the previous section should now be available in OpenStack

**Note:** The following is done with the assumption that you used the [RackSpace Private Cloud](http://www.rackspace.com/cloud/private/) distro and AlamoController is the controller.

1. Navigate to Horizon
        http://AlamoController
1. Log in with the credentials previously provided
1. Click on *Instances* on the left hand side
1. Click on *Launch Instance* on the top right hand side
1. At the *Launch Instance* window input the following
        Instance Source: Image
        Image: Windows XP SP3
        Instance Name: WinXP
        Flavor: m1.tiny
        Instance Count: 1
1. Click the *Access & Security* tab
1. Click *Windows*
1. Click *Launch*

### Associate Floating IP

1. Within the *Instances* screen, locate the Windows XP instance
1. At the end of the row click the drop down arrow and click *Associate floating IP*
1. At the *Manage Floating IP Associations* window click the drop down *Select an IP Address*
1. Select an appropriate and available IP and click *Associate*

### RDP

1. Next use your RDP client of choice and connect to the **floating IP** that was associated.

### Done
Hope that helps.

Questions/Comments/Praises can be sent to me at <joe@unicornclouds.com>
