---
layout: site
---
[]() The FCC Virtual Machine: The Fastest Way To Get Started
============================================================

[]() About virtual machines
---------------------------

A virtual machine is just like a real machine, except that the machine
hardware is emulated by software. The virtual machine, often called the
"guest", runs in a "host" operating system (OS).

To run guests on your host, you need to install an "hypervisor". For the
FCC, we decided to use an open source hypervisor called
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) .
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) can be used to
create virtual machines on which an OS can be installed.

In this tutorial, we will use
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) to load and run
a virtual ubuntu machine containing all the software needed to perform
an FCC analysis.

[]() Getting started
--------------------

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) .

Get the virtual machine, located at

    /afs/cern.ch/exp/fcc/vms/Ubuntu_14.04.3_LTS.ova

Import this virtual machine in
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) (File menu, then
Import Appliance).

Start the machine.

Follow the instructions in the README file located on the desktop of the
virtual machine.

If you want to know more, follow
[FccSoftwareEDM](./FccSoftwareEDM){.twikiLink} and
[FccSoftwareHeppy](./FccSoftwareHeppy){.twikiLink} . **Since the
installation has been done for you in the ubuntu guest, you should skip
the installation instructions** .

To get the ubuntu machine password, contact Colin.

[]() FAQ
--------

### []() My keyboard is not correctly recognized

This virtual machine was prepared with a US keyboard. If you're using
another type, you need to [configure it in the ubuntu
guest](http://www.wikihow.com/Change-Keyboard-Layout-in-Ubuntu) .

### []() How can I copy-paste on a mac with a touchpad.

Assuming you have selected some text in the ubuntu guest.

Solution 1:

-   click on your pad with two fingers, and select copy
-   click on your pad with two fingers, and select paste

Solution 2:

-   get an external mouse, and click the middle button

If you manage to emulate a middle click on the pad in the guest, please
tell Colin
![smile](https://twiki.cern.ch/twiki/pub/TWiki/SmiliesPlugin/smile.gif "smile")

### []() I'm getting messages about mouse and keyboard capture

You can safely ignore them, and google these messages if you want to
know more.

-- [<span class="wikiUser ColinBernet"> ColinBernet
</span>](/twiki/bin/view/Main/ColinBernet){.twikiLink} - 2015-12-15
