The FCC Virtual Machine: The Fastest Way To Get Started
==

About virtual machines
--

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
a virtual [CernVM](ttps://cernvm.cern.ch).

Getting started
--

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) .

Get the virtual machine `OVA` image [here](https://cernvm.cern.ch/portal/downloads).

Import this virtual machine in
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) (File menu, then
Import Appliance).

Start the machine. **The first time start will take a while**.

After initialisation, you'll be confronted with the following

```
In order to apply a cernvm-online context, use #<PIN> as username
```

FIXME: which context should we take?


To use the FCC software in the virtual machine follow the usual [tutorial](FccSoftwareGettingStarted.md).
**Make sure you setup the `/cvmfs` not the `/afs` software**.

FAQ
--

### My keyboard is not correctly recognized

This virtual machine was prepared with a US keyboard. To change the keyboard, click settings on the right in the bar
at the bottom of the screen, select Keyboard, select Layout.

### How can I copy-paste on a mac with a touchpad.

Assuming you have selected some text in the guest.

Solution 1:

-   click on your pad with two fingers, and select copy
-   click on your pad with two fingers, and select paste

Solution 2:

-   get an external mouse, and click the middle button

If you manage to emulate a middle click on the pad in the guest, please
tell Colin
![smile](https://twiki.cern.ch/twiki/pub/TWiki/SmiliesPlugin/smile.gif "smile")

### I'm getting messages about mouse and keyboard capture

You can safely ignore them, and google these messages if you want to
know more.
