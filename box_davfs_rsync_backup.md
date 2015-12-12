title: Box.net Backup Setup
date: 2013-01-11


A couple years ago [Box](http://www.box.net) ran a two month promo for iPad and iPhone users. [blog link](http://blog.box.com/2011/10/were-giving-ios-users-insane-amounts-of-free-storage-box50gb/) Luckily I was able to captalize on this free upgrade. I never utilized the service as anything more as a simple storage for a couple word documents. I believe the culprit for the under utilization of such a rather large free online storage was due to the interface of the service. It didn't feel right and was kind of a hassel to use in all honestly. That recently changed once I realized you can remotely mount your Box account as a [DAVFS](http://en.wikipedia.org/wiki/WebDAV) share. That coupled with rsync has really proven itself to be a more than succifient backup. As I go back to college to complete my degree, I'm finding the service far more useful to backup my work.

You no doubt want to accomplish the same so I have written up a bit of a walkthrough on how anyone could accomplish this. This takes into account you are running some form of Linux. In my case I use [Arch Linux](https://www.archlinux.org/) which I recommend personally.

### Prep the system

You will want to install some form of davfs support.
        sudo pacman -S davfs2

Create a directory for your Box account to be mounted to
        mkdir ~/Box

Create a config directory for Davfs2
        mkdir .davfs2

Set some config options for Davfs2
        echo "secrets   ~/.davfs2/secrets" >> ~/.davfs2/davfs2.conf
        echo "use_locks 0" >> ~/.davfs2/davfs2.conf

Set you Box credentials
        echo 'https://www.box.com/dav email@address "password in quotes"' >> ~/.davfs2/secrets
        
Set up fstab
        echo "https://www.box.com/dav /home/jkordish/Box davfs rw,user,noauto,uid=jkordish 0 0" >> /etc/fstab

Try mounting
        mount ~/Box

Running `mount` by itself now you should see a line like the following
        https://www.box.com/dav on /home/jkordish/Box type fuse (rw,nosuid,nodev,noexec,relatime,user_id=1000,group_id=100,allow_other,max_read=16384)

If that all works then you should be able to just copy files directly into the ~/Box directory now. Thats all fun and fine but you probably want to be able to sync now right?

### Rsync'ing to Box

Install rsync if you don't have it already - once again on Arch you would use pacman
        sudo pacman -S rsync grsync
        
I recommend install grsync for the gui. You click want you want to accomplish and then copy the rsync flags out to be used later. Or you can just use grsync itself. Up to you.

So I want to backup a folder into my mount'd Box account.
        rsync -r -t -v --progress --delete --modify-window=1 -c -i -s /home/jkordish/Documents/*Folder to Sync* /home/jkordish/Box
        
That should run just fine. But now we know it runs and we tested it you can go a step further and make a shell function for easy access. I personally *love* [ZSH](http://www.zsh.org/). You can do this with bash but I don't know how off the top of my head. For ZSH I created a function called upCapella which sync my Capella folder to Box
        function upCapella { command rsync -r -t -v --progress --delete --modify-window=1 -c -i -s /home/jkordish/Documents/Capella /home/jkordish/Box }
Add something similiar into your .zshrc file and source itself
        source .zshrc
You can now just run upCapella to perform a rsync whenever you want and when the Box folder has been mounted.

### Done
Hope that helps.

Questions/Comments/Priases can be sent to me at <joe@unicornclouds.com>
