# Pre-workshop checklist

:::{admonition} Learning Objectives
:class: objectives

* You will be ready for the workshop!
:::


* Follow this guide before arriving; we will do a quick introduction to environment setup
but we will not have much time to help you with problems on these issues during the workshop.
This means you will end up watching instead of participating.

* This will be an interactive workshop. In all cases (in-person or virtual tutorials) you will need to use
your own computer (for in-person events there will be no machines for you to use in the room).
You will use your own computer to connect to resources available for the tutorial (check the event
announcement for the available options).

* Follow all the steps using the computer you plan to bring, not
your desktop or someone else's computer.

* In case of a in-person event
   * Make sure that you can connect to the network in the room. For example, for events at CERN, if this is the first time you are bringing your laptop to CERN, you will have to [register it](https://information-technology.web.cern.ch/help/connect-your-device) before it can
access the internet.
   * Do not forget to bring your power supply, as well as the relevant plug adaptor, e.g., for CERN, to Swiss and European plugs.

* The FCCSW has been developed on Linux and the main platform supported is the default platform on CERN lxplus, i.e. CentOS7 .
  Experimental support for other Linux systems (e.g. Ubuntu 20.04 LTS) and MacOxS is provided as is. There is no support for Windows.

## Checking the chosen resources

Please try the following steps with the computer you will use at the workshop (the example is given for lxplus, but should hold for the other resources as well):

1. From a terminal (`xterm` on Linux or `Terminal` on Mac OS X) connect to lxplus with `ssh -X lxplus.cern.ch`.
    If your local username is different from your `lxplus` one use `ssh -X mylxplusname@lxplus.cern.ch`.
    Please try exactly this command even if you usually use an alias or other shortcut.
    >If, just below the `Password:` line, you get a message `Warning: untrusted X11 forwarding setup failed: xauth key data not generated`:
    >* Logout (using `logout` or `Ctrl-d`)
    >* Login using [`-Y`](https://man.openbsd.org/ssh#Y) instead of [`-X`](https://man.openbsd.org/ssh#X)
    >* This will switch to trusted X11 forwarding and you may see a message like `Warning: No xauth data; using fake authentication data for X11 forwarding.`
2. Check that X11 forwarding works by typing `glxgears` on lxplus. Some rotating gears should appear in
    a new window. Press `Ctrl-C` from the terminal to exit.
    >If you're not connected to the CERN network at CERN, do not worry if the X11 forwarding is slow--this is normal.

If you can successfully execute all of the above steps, you are ready to go for
the workshop!

## Enabling the FCCSW software installation from `cvmfs`

There is a complete installation of FCC software provided on `cvmfs`, which can be set up using:
```
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```


## Special notes or alternative cases / settings
### Bash shell

The [Bash shell](http://cern.ch/go/gdJ9) will be used
throughout the workshop.
The default for new computing accounts is now Bash. If you have an older
account, the default used to be a shell called `tcsh`
(“tee-cee-shell”), which has subtly different ways of doing things
in comparison with Bash.

It is recommended to change your default shell to Bash if this is the case, which is much more
widely used than `tcsh` and also supported by FCC, by visiting your
[CERN account page](https://account.cern.ch), then clicking “Resources and
services”, then “List services”, “LXPLUS and Linux”, “Settings”, then change
“Unix shell” to `/bin/bash`, and click “Save Selection”.

If you don't want to change your default shell, just execute the `bash`
command when you login to lxplus.

### Using a virtual machine through VirtualBox

The CernVM project provides a convenient tool to start VMs, [cernvm-launch](https://cernvm.cern.ch/portal/launch), and a [public repository](https://github.com/cernvm/public-contexts) of contexts to be used with `cernvm-launch` to configure the VM at your needs. The tool `cernvm-launch` is available for Linux, Mac and Windows.
A context dedicated to the FCC tutorials is available in the repository. The [cernvm-launch](https://cernvm.cern.ch/portal/launch) works with [VirtualBox](https://www.virtualbox.org/), virtualization manager available for free for all platforms.

If you have a CERN account, this is a convenient way to enable access to the EOS storage system.

To create and use a CernVM virtual machine for the FCC tutorials please follow the following steps:

   * Make sure [VirtualBox](https://www.virtualbox.org/) is installed (details installing instructions from the product web page).
   * Download the `cernvm-launch` binary for your platform either from the [dedicated download page](https://ecsft.cern.ch/dist/cernvm/launch/bin/) or from the following links:
      * [Linux](https://fccsw.web.cern.ch/fccsw/utils/vm/cernvm/launch/linux/cernvm-launch)
      * [Mac](https://fccsw.web.cern.ch/fccsw/utils/vm/cernvm/launch/mac/cernvm-launch)
      * [Win](https://fccsw.web.cern.ch/fccsw/utils/vm/cernvm/launch/win/cernvm-launch)

     Make sure is visible in your $PATH.
   * Get the [fcc-tutorial.context](https://raw.githubusercontent.com/cernvm/public-contexts/master/fcc-tutorial.context) (use wget or curl)

Once you have all this you can create the VM with this command:
```
$ cernvm-launch create --name fcc-tutorial --cpus 4 --memory 8000 --disk 20000 fcc-tutorial.context
```
You an choose how many CPU cores to use, the memory and the disk space. Good rules of thumb are to use half the cores of your machine, at least 2 GB memory per core, and enough disk for your job. The above command should oepn a window with VirtualBox and produce on the screen an output like this
```
Using user data file: fcc-tutorial.context
Parameters used for the machine creation:
        name: fcc-tutorial
        cpus: 4
        memory: 8000
        disk: 20000
        cernvmVersion: 2020.07-1
        sharedFolder: /Users/ganis
```
You see in partcular that your `$HOME` area is shared with the VM, so you can exchange files between the VM and the host machine very conveniently.

From now on you can either work in the VirtualBox window or ssh to the machine with
```
cernvm-launch ssh [username@]fcc-tutorial
```
The default user name and password are `fccuser` and `xpass`; these can be changed in the `fcc-tutorial.context` file before creating the VM. Graphics is automatically enable when connecting via ssh. Note, however, that GL-related graphics may not work on Mac hosts; for the time being the only workaround is to use directly the VirtualBox desktop.

The user has sudo privileges. Passless ssh connection can be setup as usual but needs to be enabled in `/etc/ssh/sshd_config` (editable as sudo).

The `cernvm-launch` also supports listing, stopping, starting virtual machines. Please run `cernvm-launch -h` for all the available options.

### Windows

On Windows, some additional steps are required before you can connect via SSH.
The following instructions may help in achieving this:

Set up steps (you only have to perform this once):

1. Download the [Xming installer](https://sourceforge.net/projects/xming/files/latest/download).
2. Run the installer.
3. Download [PuTTY](https://the.earth.li/~sgtatham/putty/latest/x86/putty.exe).

The following steps have to be executed each time you want to connect:

1. Start PuTTY.
2. In the list on the left, unfold `Connection` and `SSH`, then click the `X11` item.
3. In the window that appears, make sure the check box labeled `Enable X11 forwarding` is checked.
4. Return to the previous window by selecting `Session` int he list on the left.
5. In the text box labeled `Host Name (or IP address)`, type `lxplus.cern.ch`.
6. Make sure the `Port` text box contains the number `22`.
7. Click the `Open` button on the bottom of the screen.
8. A window appears with the text `login as:`. Type your CERN username, followed by Enter.
9. The window should say `Using keyboard-interactive authentication. Password:`. Type your password, again followed by Enter.
10. You now have a remote SSH session at an lxplus server node!
