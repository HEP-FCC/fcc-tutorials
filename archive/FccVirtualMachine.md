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
    - [Quick start](#quick-start)
    - [Setting up a data volume](#setting-up-a-data-volume)
    - [Getting X11 forwarding to work](#getting-x11-forwarding-to-work)
    - [Typical bash settings](#typical-bash-settings)
    - [Customizing the image](#customizing-the-image)

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

Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

> Make sure the Hypervisor network is configured correctly by going to the settings of VirtualBox and selecting Network: Under "Host-only Networks" you should see `vboxnet0`. If it is not in the list, add it with the "+" symbol on the right.

Get the virtual machine `CernVM 3.6.5  OVA` image [here](https://cernvm.cern.ch/portal/downloads).

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

You should now see an X-window session launching and be prompted with a user / password dialog box (if you still get the CLI prompt for a user name, something went wrong with the pairing, most likely you downloaded an incompatible image in the second step):

![x-session](images/FccVirtualMachine/x-session.png)


The user name `guest` and the password corresponding to the numbers one to four.

> Make sure to change the password.


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

The image is relatively large (~2 Gb), we provide versions on afs and cvmfs for you to download:

```
scp [lxplus-username]@lxplus.cern.ch:/afs/cern.ch/exp/fcc/vms/ubuntu[version]_root[version]_fcc[version].tgz [some_location]/fccimage.tgz
```

> Via lxplus you can look in the directory and make sure you download the newest version (should be last entry):<br>
`ssh [lxplus-username]@lxplus.cern.ch ls -ltr /afs/cern.ch/exp/fcc/vms/ubuntu*fcc*`

Now you need to add the image to Docker by providing the correct path to the `fccimage.tgz` below:

```
docker load -i fccimage.tgz
```

Now you'll be able to [launch your first container](#setting-up-your-development-environment-in-a-docker-container).

#### B. Building the image yourself

[Skip](#setting-up-your-development-environment-in-a-docker-container) this when you downloaded the image as detailed
above.

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

The image is described by a  Dockerfile. We have two separate layers we recommend to at least download the first image,
to avoid having to recompile ROOT (see [above](#a-downloading-the-image)):

1. Ubuntu + ROOT installation ([Dockerfile](https://github.com/HEP-FCC/fcc-spi/blob/master/docker/Dockerfile-ubuntu+root)
  and image e.g. `/afs/cern.ch/exp/fcc/vms/ubuntu16.04_root6.08.02.tgz`)
1. FCC software ([Dockerfile](https://github.com/HEP-FCC/fcc-spi/blob/master/docker/Dockerfile-fcc) and image e.g.
  `/afs/cern.ch/exp/fcc/vms/ubuntu16.04_root6.08.02_fcc0.8.tgz`)

Create an *empty* directory and download the Dockerfile(s).

```
curl https://raw.githubusercontent.com/HEP-FCC/fcc-spi/master/docker/Dockerfile-ubuntu+root -O # we recommend to skip this one
curl https://raw.githubusercontent.com/HEP-FCC/fcc-spi/master/docker/Dockerfile-fcc -O
```

Now we have to build the entire software stack from scratch. It does not matter whether you have already installed parts
of the stack on your host machine. We build everything again, within the virtual machine. This is good: It ensures a
consistent setup and that we don't mess anything up for the workflows you are used to. The downside is that this step
will take quite some time.

```
docker build -t ubuntu_root -f Dockerfile-ubuntu+root . # not needed if you downloaded it
docker build -t fccimage -f Dockerfile-fcc .
```

> **NOTE** that this may take quite some time (mainly because ROOT is rebuilt).

### Setting up your development environment in a Docker container

In Docker, containers are the actual virtual machines on which you work. Containers are created based on Docker images.
The Docker mantra is that containers are disposable: You should set up your workflow in a way that loosing a given
container will not result in lost work. To help with that, at least read [this](#setting-up-a-data-volume).

#### Quick start

For the impatient, this will get you a running docker container. For more details and settings, see the sections below.

```
docker run -ti --name fccsw -v [local directory]:/work --rm fccimage
```

You should work in `/work` as detailed [below](#setting-up-a-data-volume). You can access files with any tools on the
host (e.g. your favorite editor) in the `[local directory]` you supplied in the command.

You should now see a command prompt in the directory `/home/fccuser` (within the container):

```
+--------------------------------------------------------------------
            FCC  ##        .
           ## ## ##       ==    Welcome to the FCC software docker
        ## ## ## ##      ===    REMINDER: Containers are disposable;
    /""""""""""""""""\___/ ===            Keep your data in volumes!
 ~~{~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~
    \______ o          __/
      \    \        __/         Documentation: fccsw.web.cern.ch
       \____\______/
+--------------------------------------------------------------------
fccuser@220fd963b5d4:~$
```

The FCC software is installed in `/usr/local/fcc` and paths are already set up. Test it by trying:

```
fcc-pythia8-generate $FCCBASE/share/ee_ZH_Zmumu_Hbb.txt
```

You should see that events are generated. When the process is done you should find a file `ee_ZH_zmumu_Hbb.root`.

> **NOTE**: If you want to inspect the file with ROOT within the container you need to
[setup X11 forwarding](#getting-x11-forwarding-to-work).

#### Setting up a data volume

When launching your container you should always
[mount a host directory as a data volume](https://docs.docker.com/engine/tutorials/dockervolumes/#/mount-a-host-directory-as-a-data-volume)
by adding `-v [local directory]:/work`. The directory is then mounted in your container in `/work`. **Only files in that
directory** (or others you mounted in this fashion) **are persistent.**

Anything you want to keep should end up in that directory! I.e. code you are editing and want to compile / run should go
into that directory as well as data files.

Now let's run the container in an interactive session:

```
docker run -ti --name fccsw -v [local directory]:/work --rm fccimage
```

If you work solely in the `/work` directory you'll be able to use host-native tools (e.g. your preferred editor) to work
with the files you are using in the container.

Of course you can also mount your data volume in any other place by changing `/work` to another path, e.g. the fccuser
home-directory.

#### Getting X11 forwarding to work

If you want to use root interactively (or any other program using a GUI), you'll need to enable X11 forwarding.

**Linux**: We assume that you have an X windows server running on your host
(check that `echo $DISPLAY` gives you a non empty output). First allow local connections to the X server:

```
xhost +local:
```

Then run the docker container setting the display and mounting the X11 socket:

```
docker run -ti --name fccsw --rm -v [local directory]:/work \
       -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
       fccimage
```

**macOS**: Things are a bit more complicated due to the way XQuartz works. The only working solution we could find
requires additional software as a workaround. If you discover something that runs without socat, please let us know.

First install socat through homebrew (homebrew is a package management system for macOS, if the command does not work
you also need to install homebrew): `brew install socat`. Now we need to run socat in the background to forward calls to
the X11 socket

```
ln -fs ${DISPLAY} /tmp/x11_display
socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:/tmp/x11_display &
```

Now when running the container you need to add `-e DISPLAY=$(ipconfig getifaddr en0):0.0`, e.g.:

```
docker run -ti --name fccsw --rm -v [local directory]:/work \
       -e DISPLAY=$(ipconfig getifaddr en0):0.0 \
       fccimage
```

#### Typical bash settings

1. Adding a `bashrc`: Create your `bashrc` somewhere on the host, let's assume it is in `~/fcc/bashrc`.
  **If you plan on using your normal `~/.bashrc`, make sure you are not setting / sourcing anything that doesn't
  make sense in the container**. When launching the container add `-v ~/fcc/bashrc:/home/fccuser/.bashrc`.

1. Enabling persistent bash history: Create your history file on the host, let's assume it is in `~/fcc/bash_history`.
  You can also use your local history file, but obviously that means that the histories will mix. When running the
  container add `-v ~/fcc/bash_history:/home/fccuser/.bash_history`.

#### Customizing the image

Finally you have the option of adding layers on top of the provided image (e.g. to install an editor if you want to
edit things via the CLI rather than using host-native tools). For that we refer you to the
[docker documentation](https://docs.docker.com/engine/reference/builder/).

The easiest way will be to write your own `Dockerfile` and install the packages you need, e.g. for vim:

```
FROM fccimage
RUN sudo apt-get install -y vim
```

And build a new image from this file with docker: `docker build -t myfccimage -f [Dockerfile] .`

> We strongly recommend to have a close look at the Docker documentation if you decide to do this.
