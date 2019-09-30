
# Getting started with FCC software

The FCC software is the common software for the FCC detector design study. We support the whole chain starting
from event generation through parameterized and full detector simulation, reconstruction and data analysis.

### Prerequisites

You should be familiar with basics of `bash` and know something about either python or C++ programming. If you are not, there are excellent material on the web.

New to CERN? Get to know the lxplus system [here](http://information-technology.web.cern.ch/book/lxplus-service/lxplus-guide/lxplus-aliases), [here](http://information-technology.web.cern.ch/services/lxplus-service), and [here](https://twiki.cern.ch/twiki/bin/view/LHCb/RemoteLxplusConsoleHowTo). Log in with the standard `ssh` command; if you are on Windows, look at [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).

> When you plan to contribute, have a look at the [contribution guide](./FccSoftwareGit.md).

## Setting up the FCC environment


The following  will set up the pre-installed software on lxplus (or any centos7 machine with cvmfs, e.g. lxplus):

```bash

source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
```

*Note*: This has to  be done every time you start a new session (i.e. when you log into your machine).

Check the setup by looking for the command `fccrun` to run jobs in the Gaudi-based software framework FCCSW:

```
which fccrun
```

### Alternative setup methods

* The above script should automatically choose the latest installation available.
For productions it is recommended to explicitly choose the version and platform of the software to use, for example by running
```
source /cvmfs/fcc.cern.ch/sw/views/releases/externals/94.2.0/x86_64-centos7-gcc62-opt/setup.sh
```

Note that the above only sets up the "externals" and not the FCC software framework.
This must be done in another step, running (fox example):
```
/cvmfs/fcc.cern.ch/sw/releases/fccsw/0.10/x86_64-centos7-gcc62-opt/this_fccsw.sh
```
Note that the `this_fccsw.sh` script is called `setup.sh` in versions of FCCSW newer than `0.10`. 

* In case you want to work offline or need to tweak something deep in the stack, take a look at this repository of [FCC packages for Ubuntu ](https://fcc-pileup.web.cern.ch/fcc-pileup/sw/fcc-ubuntu-sw.html).

### Using Virtual Machines or Docker containers

The instructions above should work in any CentOS7 virtual machine or Docker container with `cvmfs` available. We give in the following one example for each of the two cases.

#### CernVM Virtual Appliance

The CernVM project provides a convenient tool to start VMs, [cernvm-launch](https://cernvm.cern.ch/portal/launch), and a [public repository](https://github.com/cernvm/public-contexts) of contexts to be used with `cernvm-launch` to configure the VM at your needs. A context dedicated to the FCC tutorials is available in the repository. The [cernvm-launch](https://cernvm.cern.ch/portal/launch) works with [VirtualBox](https://www.virtualbox.org/), virtualization manager available for free for all platforms.

To create and use a CernVM virtual machine for the FCC tutorials please follow the following steps:

   * Make sure [VirtualBox](https://www.virtualbox.org/) is installed (details installing instructions from the product web page).
   * Download the `cernvm-launch` binary for your platform from the [dedicated download page](https://ecsft.cern.ch/dist/cernvm/launch/bin/); make sure is visible in your $PATH
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
	cernvmVersion: 2019.06-1
	sharedFolder: /Users/ganis
```
You see in partcular that your $HOME area is shared with the VM, so you can exchange files between the VM and the host machine very conveniently.
From now on you can either work in the VirtualBox window or ssh to the machine with
```
cernvm-launch ssh fcc-tutorial
```
In either case you need a user name and password, which by default are `fccuser` and `fccpass`; these can be changed in the `fcc-tutorial.context` file.
Note that the SSH session currently does not support graphics.
The `cernvm-launch` also supports listing, stopping, starting virtual machines. Please run `cernvm-launch -h` for all the available options.

#### LHCb CentOS7 Docker image

In case you don't have a centos7 installation, but you do have docker, you can use the [centos7 docker image provided by LHCb](https://gitlab.cern.ch/lhcb-core/LbDocker/#usage).
Invoking `lb-docker-run --centos7 --no-lblogin --force-cvmfs` should give you access to the fcc cvmfs installations even if your host machine does not have cvmfs installed.


<!-- ![flow-chart getting started](./images/FccSoftwareGettingStarted/flow_chart_starting.png) -->

## Where do I start?

That of course depends on what you want to do:

### Produce and analyse fast-simulated events:

- [Getting started with the production and analysis of fast-simulated events](FccSoftwareGettingStartedFastSim.md)
    - [Getting started with papas (FCC\-ee)](FccSoftwareGettingStartedFastSim.md#getting-started-with-papas-fcc-ee)
    - [Getting started with Delphes (FCC\-hh)](FccSoftwareGettingStartedFastSim.md#getting-started-with-delphes-fcc-hh)

### Develop or use full simulation, reconstruction and detailed detector descriptions:

- [Getting started with FCCSW](./FccSoftwareFramework.md)
- [Geant 4 full (and fast) simulation](https://github.com/HEP-FCC/FCCSW/tree/master/Sim/doc/README.md)
- [Getting started with detector description](https://github.com/HEP-FCC/FCCSW/tree/master/Detector/doc/DD4hepInFCCSW.md)
- Reconstruction
    - [Information about calorimeter reconstruction](https://github.com/HEP-FCC/FCCSW/tree/master/Reconstruction/doc/RecCalorimeter.md)
    - [Information about track reconstruction](https://acts.web.cern.ch)
- For information about using Delphes, see the [FCC-hh example](FccSoftwareGettingStartedFastSim.md#getting-started-with-delphes-fcc-hh) mentioned above

Additional information is to be found in the [index](README.md)
 
## Where do I find more information?

Depending on what you want to do, there are three different repositories that are your entry point in the FCC software stack.

The [tutorials overview](http://fccsw.web.cern.ch/fccsw/tutorials) has links to further reading material grouped by repository.

The following panels should help you identify where to look for more:

### Look at [heppy & fcc-physics](http://fccsw.web.cern.ch/fccsw/tutorials#further-reading) for:

Analysis and fast simulation

- Standalone Pythia event generation
- FCC-ee parametric fast simulation (papas)
- FCC-ee and FCC-hh physics analysis
 
### Look at [FCCSW](http://fccsw.web.cern.ch/fccsw/tutorials#further-reading) for:
 
Event generation, simulation and reconstruction

- Event generation with Pythia (more to come)
- FCC-hh parametric fast simulation (Delphes)
- Full and fast simulation with Geant 4
- Detector descriptions with DD4hep
- Reconstruction algorithms

***

If you encounter problems or have ideas for improving our tutorials, please contact FCC developers  on mattermost, the forum or via mailing-list. Find the links on [https://cern.ch/fccsw](https://cern.ch/fccsw) !
