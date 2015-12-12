title: Using MergeIDE (Converting Windows XP VMDK to KVM)
date: 2013-04-05

# Why?
If you want to convert a VMware Windows XP VMDK over to something like KVM there is a weird step to convert the disk controller interface over to IDE.

## Mergeide

To do so is fairly simple as a matter of running MergeIDE on the machine. You may either download/copy the registry file over. But for future use you may want to create a small floppy image with the files already on it.

### Download Merge IDE

You will first need to obtain MergeIDE.

1. Download [MergeIDE](http://www.virtualbox.org/attachment/wiki/Migrate_Windows/MergeIDE.zip)
    $ wget http://www.virtualbox.org/attachment/wiki/Migrate_Windows/MergeIDE.zip

### Create Floppy Image

We create a small floppy image and copy the contents of MergeIDE on to it. This allows us to attach it to our virtual machine later.
1. Create floppy image
    $ mkfs.msdos -C MergeIDE.img 1440

    Note: mkfs.msdos needs to be installed. If you run Arch Linux it is part of the dosfstools package
1. Mount the MergeIDE.img Floppy image
    $ sudo mount -o loop MergeIDE.img /mnt
1. Copy the MergeIDE folder over to the floppy
    $ cd /mnt && sudo unzip <path to MergeIDE.zip> && cd -
1. The contents from the zip file should be on the floppy image now.
1. unmount floppy
    $ sudo umount /mnt

### Run MergeIDE

1. Attach the floppy image to the Windows XP image and boot.
    $ qemu-system-x86_64 --enable-kvm -m 2048 -hda WINXP.qcow2 -fda MergeIDE.img
1. Once it has booted. Login
1. Start a command prompt
    Start => Run => cmd
1. Merge the registry file
    > A:
    > reg import MergeIDE.reg

### Reboot

You should just reboot now.

### Done
Hope that helps.

Questions/Comments/Praises can be sent to me at <joe@unicornclouds.com>
