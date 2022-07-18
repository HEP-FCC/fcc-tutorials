# FCCee Interaction Region Backgrounds

:::{admonition} Learning objectives
:class: objectives

* get to know tools to  study FCCee interaction region backgrounds
* know how to setup and use GuineaPig
:::


## Using Guinea-Pig to generate interaction region backgrounds 


Guinea-Pig is included in releases of the FCC software and is developed at this repository: 

<https://gitlab.cern.ch/clic-software/guinea-pig>

Issues and Pull Requests can be submitted there.


### Generating e- e+ pairs 

In order to run Guinea-Pig (hereafter GP) and generate e- e+ pair background, one should provide the relevant accelerator (beam) parameters, plus some steering parameters to run the software. Those parameters are set in the file acc.dat.
Currently, one can find the four following accelerators, where the beam parameters correspond to the values considered for FCC CDR (2019).
- FCCee Z working point (Ecm = 91.2 GeV): FCCee_Z
- FCCee W working point (Ecm = 160 GeV): FCCee_W
- FCCee ZH working point (Ecm = 240 GeV): FCCee_ZH
- FCCee Top working point (Ecm = 365 GeV): FCCee_Top

and the following 2 sets of configuration parameters:
- FCCee_Z
- FCCee_Top

It is recommended to run the FCCee Z accelerator together with the FCCee_Z parameters, while the other 3 accelerators can be run with the FCCee_Top parameters.

To run GP you should type the following:

```bash
guinea $ACC #PAR output
```

e.g.

```bash
guinea FCCee_Z FCCee_Z output
```

`output` it is the produced log file, and it can be given any name. Below we will try to explain the main GP configuration parameters. Each GP run corresponds to 1 bunch crossing.

#### GP configuration parameters

### Generating large amount of data with GP

One can use the script at:

<https://github.com/Voutsi/FCCee_IR_Backgrounds/blob/master/eepairs/sub_gp_pairs.sh>

that sends a user defined number of bunch crossings to be generated in parallel in Condor. You should modify accordingly the following parts of the script:

```bash
nruns=100
```

defines the number of bunch crossings to be generated

```bash
ROOTDIR=/afs/cern.ch/user/v/voutsina/Work/FCCeeBKG_WrapUp/eepairs
```

This variable defines the directory where the results will be stored. The script will generate there a new directory, data${i} for the ith generated bunch crossing.

Command

```bash
sed -i -e 's/rndm_seed=1/rndm_seed='${nn}'/g' acc.dat
```

Changes the random seed for the ith bunch crossing according to the pattern

```bash
    nn=${i}*100000
```

Feel free to modify the pattern, but have in mind that if you run N BXs with the same seed, you will generate N times the same data.

In the following line

```bash
/afs/cern.ch/user/v/voutsina/Work/testarea/CodeTest/GP++/guinea-pig.r3238/src/guinea FCCee_Top FCCee_Top output
```

you should replace the path where your guinea executable is located, the desired accelerator and configuration-parameters names and the desired output file name.

The queueing in Condor is defined by the following line

```bash
+JobFlavour = "tomorrow"
```

For the set of parameters FCCee_Z, featuring an estimating running time of few hours, a job flavour "workday" is recommended. For the  set of parameters FCCee_Top, job flavour "longlunch" should be enough.

#### Analysing the data (only for ILCSOFT users)

Marlin processors used to analyse the simulated data. They were used for CDR results.
In order to compile them: please initialise ILCSoft environment first.

```bash
mkdir build; cd build
cmake -C $ILCSOFT/ILCSoft.cmake ..
make install
```

### GP production of `$\gamma\gamma$`hadrons

In order to produce `$\gamma\gamma$` to hadrons with GP, we need to add the following commands inside the configuration file acc.dat

```bash
hadron_ratio=100000;
do_hadrons=3;
store_hadrons=1;
```

while switching off pair production:

```shell
do_pairs= 0;
```

`do_hadrons = 3;` will make GP to produce a hadron.dat file, which contains the produced partons, with the same cross-section parametrisation as Pythia does. "hadron_ratio=100000;" is the weight factor with which the cross section of the
hadronic interaction is scaled. As a second step, we invoke Pythia to do the fragmentation. To do so, we use the "hades" library from Daniel Schulte, which allows to feed the GuineaPig's output to Pythia. Finally we translate the Pythia's output to .HEPEvt style events. To perform the last 2 steps, we can use the tar file at


<https://github.com/Voutsi/FCCee_IR_Backgrounds/blob/master/ggToHadrons/hadron.tar.gz>

This file was made by Dominik Arominski, and contains the HADES library. Please unpack it and follow the instructions given in the README file.
