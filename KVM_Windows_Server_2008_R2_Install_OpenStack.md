title: Windows 2008 Server R2 install guide for KVM and OpenStack
date: 2013-06-05

# Prerequisite

In order to install the Windows Server 2008 R2 Operating System you will require the following:

1. KVM is already up and running properly.
2. You have a copy of the Windows Server 2008 R2 iso
        $ sudo dd if=/dev/cdrom of=Window_Server_2008_R2.iso
3. You have the Windows Server 2008 R2 Product License available
4. Download the iso disk image of the Virtio Drivers
        $ wget https://launchpad.net/kvm-guest-drivers-windows/20120712/20120712/+download/virtio-win-drivers-20120712-1.iso
    Note: I like the Ubuntu iso as compared to the RedHat one.

## Install Windows Server 2008 R2

The following steps should help you install Windows Server 2008 R2 and upload it into glance for use with OpenStack.

### Create Windows Server 2008 R2 Hard Drive

You will first be required to create a target hard drive to install the Windows Server 2008 R2 Operating System on.

        $ cd ~ && mkdir KVM && cd KVM

        $ qemu-img create -f qcow2 WIN2K8R2.qcow2 25G

### Attach ISO and boot

Next we will attach the Windows Server 2008 R2 ISO and boot

    $ qemu-system-x86_64 --enable-kvm -m 2048 -boot d -drive file=WIN2K8R2.qcow2,if=virtio -cdrom Win2K8X64R2Ent.iso -drive file=virtio-win-drivers-20120712-1.iso,media=cdrom -net nic,model=virtio -net user

    Note: You *must* ensure you tell it to use the **virtio** drivers

### Load Drivers & Install Operating System

1. Click Install
1. Select your Operating System type
1. Accept License Terms
1. Select Custom Installation
1. Click 'Load Driver'
1. Click Browse
1. Navigate to the cdrom 'Virtio Drivers'
    You should see two cdroms attached. One is the install cdrom and the other the 'Virtio Drivers'
1. Select 'Virtio Drivers' => STORAGE => SERVER_2008_R2 => AMD64
1. Click OK
1. The 'Red Hat VirtIO SCSI controller' driver should be highlighted. If not then you have done something wrong.
1. Click Next
    Driver should load without error and take you back to the screen to select the hard drive to install the Operating System on
1. Click 'Drive options'
1. Click 'New'
    Ensure the entire drive space is being used - in our case the entire 25G
1. Click 'Apply'
1. Click 'OK'
1. Click 'Next'
    The Operating System will install. This process may take awhile depending on resources you gave initially. Be patient.
1. Once completed you should be prompted to changed the Administrator password. Do so now.
1. The install should be completed and log you in! Congrats.

### Set your Date and Time

You should probably go ahead and set your Date and Time

1. From the 'Initial Configuration Tasks' screen
1. Click 'Set time zone'
1. From the 'Date and Time' window Click 'Change time zone...'
1. From the 'Time zone:' drop-down select your time zone.
1. Click 'OK'
1. Click 'OK'

### Enable Remote Desktop

You will want to enable *Remote Desktop*

1. From the 'Initial Configuration Tasks' screen
1. Scroll down to '3. Customize This Server'
1. Click 'Enable Remote Desktop'
1. At the 'System Properties' window the 'Remote' tab under 'Remote Desktop' select your preferred level
    For my purposes I selected the middle option - the 'less secure' option
1. Click 'OK'

### Configure the Firewall

You might want to take this time to configure the firewall. For my purposes I went ahead and disabled the Windows Firewall. This is a lab image and firewall will be taken care of at the network layer and at the perimeter. I'm not to worried about it here on the host level.

1. From the 'Initial Configuration Tasks' screen
1. Scroll down to '3. Customize This Server'
1. Click 'Configure Windows Firewall'
1. At the 'Windows Firewall' click 'Turn Windows Firewall on or off'
1. At the 'Customize setting for each type of network'
1. Click 'Turn off Windows Firewall (not recommend)' for both Private and Public locations.
1. Click 'OK'

### Turn-Off The Initial Configuration Tasks window

You will probably want to disable the annoying 'Initial Configuration Tasks' window from bombarding you every time you login.

1. From the 'Initial Configuration Tasks' screen
1. At the bottom of the window. Check the box for 'Do not show this window at logon'
1. Click 'Close'

### Install Additional Drivers

The 'Sever Manager' Console should be showing up after you closed out the 'Initial Configuration Task' Window. You should now take the time to install the VirtIO Balloon Driver.

1. Expand 'Diagnoistics' from the left hand window pane
1. Select 'Device Manager'
1. From the top menu click 'Action'
1. Select 'Add Legacy Hardware'
1. At the 'Add Hardware' window click 'Next'
1. Click 'Install the hardware that I manually select from a list (Advanced)'
1. Click 'Next'
1. Leave 'Show All Devices' select - Click 'Next'
1. Click 'Have Disk...'
1. Click 'Browse'
1. From the VirtIO CD - Locate Balloon => Server_2008_R2 => AMD64
1. Click 'Open'
1. Click 'OK'
1. 'VirtIO Balloon Drive' should be highlighted - Click 'Next'
1. Click 'Next'
1. When prompted - select 'Install this driver software anyway'
1. Click 'Finished'

Note: You should really follow the previous steps to ensure the VirtIO Network and Serial drivers are installed as well. It all should be fairly straight forward at this point.

### Shutdown

At this point you will want to shutdown the virtual machine. Go ahead and do so
.
## Importing into Glance

The following steps outline how you would import the previously created Windows XP image into Glance to be used as a instance type within OpenStack

### Upload into Glance
You can also import this completed virtual machine into Glance so that it may be used for instance deployment within OpenStack

**Note:** The following is done with the assumption that you used the [RackSpace Private Cloud](http://www.rackspace.com/cloud/private/) distribution and AlamoController is the controller.

* If another method was used then you will have to download the 'OpenStack RC File' which can be obtain from Horizon e.g. https://Horizon/settings/project/

1. Copy the image over to AlamoController
        $ scp  WIN2K8R2.qcow2 admin@AlamoController:~
**Note:** you will have to enter the admin credentials
1. Log in to AlamoController
        $ ssh admin@AlamoController
**Note:** you will have to enter the admin credentials
1. Change to root
        $ sudo -i
1. Load the OpenStack credentials
        # source openrc
1. Navigate back to the admin home directory since that is where you just scp'd the image to
        # cd ~admin
1. Upload image into Glance
        # glance image-create --name "Window Server 2008 R2" --is-public=true --disk-format=qcow2 --container-format=ovf --file WIN2K8R2.qcow2

### Security Rules

If you haven't already, prior to launching the Windows Instance you will need to ensure the remote desktop port is allowed.

1. Create 'Security Group'
    # nova secgroup-create Windows "Windows Ports"
1. Add firewall rule for the remote desktop port
    #nova secgroup-add-rule Windows tcp 3389 3389 0.0.0.0/0
1. Ensure you enable this group for your instance otherwise remote desktop won't work.

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
