
# An introduction to FCC Software

:::{admonition} Learning Objectives
:class: objectives

- Learn the key concepts needed to work with the FCC software
- Learn how to launch the FCC software with `fccrun`
:::

Imagine you want to design and run a new particle detector.
Apart from organizing a collaboration, creating the design and specification, and several other tasks, you will also have to find solutions to many computational challenges.
It's worth thinking about these for a second:

 - How do we collect data as it is recorded by the detector?
 - How do we filter and process the recorded data efficiently?
 - How do we manage all the complex tasks required to work with collision data?
 - How do we organize all the data of a single bunch crossing in a flexible way?
 - How do we configure our software flexibly without having to recompile it?
 - Can you think of more?

How would you go about solving these?
The decisions you make will affect the performance of your experiment during datataking and analysis.

At FCC, we base our software on the [Gaudi](https://gaudi.web.cern.ch/gaudi/) framework, which was specifically designed with the above questions in mind.
It's worth getting an idea of some of the most important Gaudi concepts at this point.
After this, we will jump right into running the software and getting useful things done.

**Event Loop:**
Because the individual bunch crossings (events) are almost completely independent of each other, it makes sense to process them one by one, without holding them all in memory at once.
Gaudi provides a global EventLoop, which allows you to process events one by one.

**Transient Event Store:**
A single event contains lots of different data objects (Particles, Vertices, Tracks, Hits).
In Gaudi, these are organized in the Transient Event Store (TES).
You can think of it as a per-event file system with locations like `/Event/Rec/Track/Best` or `/Event/Phys/MyParticles`.
When running over the event stream, Gaudi allows you to get and put from/to these locations.
The contents of the TES are emptied at the end of the processing of each event.

**Algorithms:**
An *Algorithm* is a C++ class that can be inserted into the EventLoop.
These allow you to perform a certain function for each event (like filtering according to trigger decision, reconstructing particles).

**Tools:**
Often, algorithms will want to make use of some common function (vertex fitting, calculating distances, associating a primary vertex).
These are implemented as *Tools*, which are shared between Algorithms.

**Options:**
To make all of this configurable, Gaudi allows you to set properties of *Algorithms* and *Tools* from a Python script, called an *option* file.
In an option file, you can specify which Algorithms are run in which order, and set their properties (strings, integers, doubles, and lists and dicts of these things can be set).
You can then start the Gaudi EventLoop using this option file, and it will set up and run the corresponding C++ objects with specified settings.

You can find comprehensive documentation in the [Gaudi Doxygen](https://gaudi.web.cern.ch/gaudi/doxygen/v30r3/index.html) or the [Gaudi Manual](https://gaudi.web.cern.ch/gaudi/resources/GUG.pdf).

Usually, you will work with one of the FCC software framework FCCSW that are based on Gaudi.
One of the most important ones is *DaVinci*, which provides lots of *Algorithms* and *Tools* for physics analysis.



You can run gaudi using the following command [on lxplus](prerequisites.md):



```bash
source /cvmfs/fcc.cern.ch/sw/latest/setup.sh
echo "from Configurables import ApplicationMgr" > option.py
fccrun option.py
```

`ApplicationMgr` is a component that sets up the EventLoop.
You should get the following output:

```
====================================================================================================================================
                                                   Welcome to ApplicationMgr (GaudiCoreSvc v32r2)
                                          running on lxplus707.cern.ch on Thu Sep 19 14:17:08 2019
====================================================================================================================================
ApplicationMgr       INFO Application Manager Configured successfully
HistogramPersis...WARNING Histograms saving not required.
ApplicationMgr       INFO Application Manager Initialized successfully
ApplicationMgr       INFO Application Manager Started successfully
EventSelector        INFO End of event input reached.
EventLoopMgr         INFO No more events in event selection 
ApplicationMgr       INFO Application Manager Stopped successfully
EventLoopMgr         INFO Histograms converted successfully according to request.
ToolSvc              INFO Removing all tools created by ToolSvc
ApplicationMgr       INFO Application Manager Finalized successfully
ApplicationMgr       INFO Application Manager Terminated successfully
```

During this run, FCCSW didn't do anything: We didn't specify any algorithms to run or any data to run over.

An `option.py` is just a regular Python script that specifies how to set things up in the software.
Many of the following lessons will teach you how to do something with FCCSW by showing you how to write or extend an `options.py`.
You can use the above command to test it.
You can also specify several option files like this:
```
fccrun options1.py options2.py
```
They will then both be used to set up FCCSW.

Do you want to get an overview of which Components of FCCSW exist? Use
```bash
fccrun --list
```

You can then look components up on [github](https://github.com/HEP-FCC/FCCSW) to find more information.
However, it is advised to follow this tutorial, as many of the components are introduced here and used in example jobs.


:::{admonition} `fccrun` and command line arguments
:class: callout

`fccrun` is a wrapper around a gaudi script called `gaudirun.py`. `fccrun` makes it easier to configure jobs on the command line. It is a dynamic script, i.e. it command line options depend on the options file and let you modify `options.py` without opening an editor.
Take a look at the example job to run Pythia8:

```shell
less $FCCSW/Examples/options/pythia.py
```
and compare it with the command line options for fccrun:
```shell
fccrun $FCCSW/Examples/options/pythia.py -h
```
And note that you have to give an `options.py` as the first argument to `fccrun` in order for this to work:

```shell
fccrun -h
```
:::
