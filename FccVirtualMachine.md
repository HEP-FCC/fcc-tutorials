The FCC Virtual Machine: The Fastest Way To Get Started
==

**Contents**
<!-- TOC -->

- [Introduction:](#introduction)
- [Using VirtualBox](#using-virtualbox)
  - [Getting started](#getting-started)
  - [FAQ](#faq)
    - [My keyboard is not correctly recognized](#my-keyboard-is-not-correctly-recognized)
    - [How can I copy-paste on a mac with a touchpad.](#how-can-i-copy-paste-on-a-mac-with-a-touchpad)
    - [I'm getting messages about mouse and keyboard capture](#im-getting-messages-about-mouse-and-keyboard-capture)
- [Using Docker](#using-docker)
  - [Setting up Docker](#setting-up-docker)
  - [Adding the FCC image to Docker](#adding-the-fcc-image-to-docker)
    - [A. Downloading the image](#a-downloading-the-image)
    - [B. Building the image yourself](#b-building-the-image-yourself)
  - [Setting up your development environment in a Docker container](#setting-up-your-development-environment-in-a-docker-container)

<!-- /TOC -->

## Introduction:

A virtual machine is just like a real machine, except that the machine
hardware is emulated by software. The virtual machine, often called the
"guest", runs in a "host" operating system (OS).

To run FCC software through a virtual machine on your laptop, you have two different options:

1. [Use VirtualBox and CVMFS](#using-virtualbox) (the CernVM distributed filesystem):
  - Quick to set up
  - Offline work may not work 100% reliably
2. [Use Docker and Spack](#using-docker), will download and install the software on setup
  - Need to download large image / slow first setup
  - After setup no need to be online

## Using VirtualBox

Traditionally, to run guests on your host, you need to install an "hypervisor". For the
FCC, we decided to use an open source hypervisor called
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) .
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) can be used to
create virtual machines on which an OS can be installed.

In this tutorial, we will use
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) to load and run
a virtual [CernVM](ttps://cernvm.cern.ch).

### Getting started

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) .

Get the launch utility from CernVM [here](http://cernvm.cern.ch/portal/launch).

This utility allows you to launch a CernVM from the command line.


Get the virtual machine `OVA` image [here](https://cernvm.cern.ch/portal/downloads).

Import this virtual machine in
[VirtualBox](https://www.virtualbox.org/wiki/Downloads) (File menu, then
Import Appliance).

Start the machine. **The first time start will take a bit longer**.

After initialisation, you'll be confronted with the following

```
In order to apply a cernvm-online context, use #<PIN> as username
```

For the moment you will have to log in the [CernVM Online](https://cernvm-online.cern.ch) system, go to `Marketplace` and
select `Experimental` at the bottom. You'll see a couple of contexts, click on the one named `FCC` and click on `pair`.
The number shown is what you'll need to insert prefixed with `#` in the command prompt of your VM.

This will launch a SLC6 environment with a user `guest` and the password corresponds to the numbers one to four. Make
sure to change the password.


To use the FCC software in the virtual machine follow the usual [tutorial](FccSoftwareGettingStarted.md).
**Make sure you setup the `/cvmfs` not the `/afs` software**.

### FAQ

#### My keyboard is not correctly recognized

This virtual machine was prepared with a US keyboard. To change the keyboard, click settings on the right in the bar
at the bottom of the screen, select Keyboard, select Layout.

#### How can I copy-paste on a mac with a touchpad.

Assuming you have selected some text in the guest.

Solution 1:

-   click on your pad with two fingers, and select copy
-   click on your pad with two fingers, and select paste

Solution 2:

-   get an external mouse, and click the middle button

If you manage to emulate a middle click on the pad in the guest, please
tell Colin
![smile](https://twiki.cern.ch/twiki/pub/TWiki/SmiliesPlugin/smile.gif "smile")

#### I'm getting messages about mouse and keyboard capture

You can safely ignore them, and google these messages if you want to
know more.


## Using Docker

### Setting up Docker

[Docker](https://www.docker.com) images are light-weight virtual machine images that can be easily distributed. To start, you'll have to
download and install docker. Here you'll find instructions for your operating system of choice:
[macOS](https://docs.docker.com/engine/installation/mac/), [ubuntu](https://docs.docker.com/engine/installation/linux/ubuntulinux/)
(check the menu on the left for different linux distributions), or [windows](https://docs.docker.com/engine/installation/windows/).
Make sure that your docker environment is working as expected by following the
[instructions to verify the installation](https://docs.docker.com/engine/getstarted/step_one/#/step-3-verify-your-installation).


### Adding the FCC image to Docker

#### A. Downloading the image

The image is relatively large (~ Gb) but we provide versions on afs and cvmfs for you to download:

```
scp [lxplus-username]@lxplus:/afs/cern.ch/exp/fcc/vm/... FIXME!
```

Now you need to add the image to Docker by:

```
docker load -i fccimage.tgz
```

If you'd prefer to only download the image description text file and build yourself, have a look
[below](#building-the-image-yourself).

#### B. Building the image yourself

<div class="panel panel-warning">
    <div class="panel-heading"><h3 class="panel-title">
        <span class="glyphicon glyphicon-info-sign" aria-hidden="true"> </span>
        Warning
    </h3></div>
    <div class="panel-body">
     <p>Building the Docker image may take a long time (depending on your machine) and if you don't know what you
are doing (and things go wrong), it may fill your disk (due to "dangling images"). If you decide to go this route, we
recommend to have a close look at the Docker documentation.</p>
    </div>
</div>

The image is described by a simple [text file]() FIXME: Add link!

```
curl ... -o Dockerfile
```

Now we have to build the entire software stack from scratch. It does
not matter whether you have already installed parts of the stack on your machine. We build everything again, within
the virtual machine. This is good: It ensures a consistent setup and that we don't mess anything up for the workflows
you are used to. The downside is that this step will take quite some time

```
docker build -t fccimage:v1 .
```

> **NOTE** that this will take quite some time (mainly because ROOT is rebuilt).

### Setting up your development environment in a Docker container

In Docker, containers are the actual virtual machines on which you work.  Containers are created based on Docker images.

It may be useful to
[mount a host directory as a data volume](https://docs.docker.com/engine/tutorials/dockervolumes/#/mount-a-host-directory-as-a-data-volume).
This allows you to use your native text editor but then build and run the software in the container.

Now you can run an interactive session:

```
docker run -i [-v [local director]:/work] --rm fccimage #-v to attach a volume
```

Now you have an open bash session and you can work as normal, but you want to make sure you keep anything you want to save
on `/work`.
