# Central production of events

The central production of events for FCC physics studies is done using the
[EventProducer](https://github.com/HEP-FCC/EventProducer) framework.

:::{admonition} Get in touch with coordinators
:class: prereq
In order to use the [EventProducer](https://github.com/HEP-FCC/EventProducer),
please get in contact with the FCC software and computing coordinators as
running central production of events requires specific rights
[(see here)](https://hep-fcc.github.io/FCCSW/computing/computing.html).

When samples produced by the [EventProducer](https://github.com/HEP-FCC/EventProducer)
framework are ready they will appear on this
[web-page](http://fcc-physics-events.web.cern.ch/).
:::


## Clone and initialisation


If you do not attempt to contribute to the repository, simply clone it:

```shell
git clone git@github.com:HEP-FCC/EventProducer.git
```

If you aim at contributing to the repository, you need to fork and then clone the forked repository:

```shell
git clone git@github.com:YOURGITUSERNAME/EventProducer.git
```

Then initialise:

```shell
source ./init.sh
```

In order to run batch generation, please add your CERN user name to the userlist in `config/users.py`

## Generate LHE files from gripacks

To send jobs starting from a gridpack that does not exist but that you have produced, do the following:
   - place gridpack on eos
     - for FCC-hh `/eos/experiment/fcc/hh/generation/gridpacks/`
     - for FCC-ee `/eos/experiment/fcc/ee/generation/gridpacks/`
   - if the gridpack is from Madgraph, name it `mg_process` (and call option `gp_mg` when running generation commands), if from powheg please name it `pw_process` (and call option `gp_pw`),
   - add to `config/param_FCCee/hh.py` an entry corresponding to the gridpack name in the `gridpacklist` list, depending on the study.

If the gridpack already exists and has been properly added to the correct `config/param_FCCee/hh.py`, then simply run:

```shell
python bin/run.py --FCCee --LHE --send --condor --typelhe gp_mg -p <process> -n <nevents> -N <njobs> -q <queue> --prodtag <prodtag> --detector <detector>
```

example to send 10 jobs of 10 000 events of ZHH events at 365GeV using the longlunch queue of HTCondor for FCC--ee for the spring2021 production tag and the IDEA detector:

```shell
python bin/run.py --FCCee --LHE --send --condor --typelhe gp_mg -p mg_ee_zhh_ecm365 -n 10000 -N 10 -q longlunch --prodtag spring2021 --detector IDEA
```

The options `--ncpus` and `--priority` can also be specified to increase the numbers of cpus on the cluster and to change the priority queue.


## Generate LHE files directly from MG5


To send jobs directly from MG5, you need a configuration file (see in `mg5/examples` directory `*.mg5`) and, optionally:
   - a `cuts.f` file (containing additional cuts)
   - a model (see in `models` directory for instance)

:::{admonition} Nota Bene
:class: callout

At the moment no example is generated for FCC-ee this way. Below is an example
for FCC-hh.
:::

As before, you need to add the process to the `config/param_FCChh.py` file. Then you can run with the following command:

```shell
python bin/run.py --FCC --LHE --send --condor --typelhe mg -p mg_pp_hh_test --mg5card mg5/examples/pp_hh.mg5 --model mg5/models/loop_sm_hh.tar -N 2 -n 10000 -q workday  --memory 16000. --disk 8000.
```

The options `--ncpus` and `--priority` can also be specified to increase the numbers of cpus on the cluster and to change the priority queue.

## Generate STDHEP files directly from Whizard + Pythia6

This section describe how to send Whizard + Pythia6 jobs and produce STDHEP files. The steps to be followed can be described as:
1. Define process in `gridpacklist` in `config/param_FCCee/.py`.
2. Write the Whizard sin card and put it in: `/eos/experiment/fcc/ee/generation/FCC-config/<prodtag>/FCCee/Generator/Whizard/<version>` by making a Pull Request to the corresponding production tag branch of [FCC-config](https://github.com/HEP-FCC/FCC-config/) for example `wzp6_ee_eeH_ecm240.sin`
3. Once the Pull Request is approved and the file has appeared on the corresponding `<prodtag>` on `eos`
4. Send jobs

```shell
python bin/run.py --FCCee --STDHEP --send --typestdhep wzp6 --condor -p <process> -N <njobs> -n <nevents> --prodtag <prodtag> -q <queue>
```

Example produce 1 job of 10000 events of mumuH at FCC-ee 240GeV

```shell
python bin/run.py --FCCee --STDHEP --send --typestdhep wzp6 --condor -p wzp6_ee_mumuH_ecm240  -N 1 -n 10000 --prodtag spring2021 -q longlunch
```

## Generate EDM4hep files from the LHE and decay with Pythia8

1. If you want to let Pythia decay without specifying anything, you can use the default card, but if you have requested extra partons at matrix element, you might need to specify matching parameters to your pythia card
2. If you want to use a specific decay, make sure that the decay you want is in `decaylist` and `branching_ratios` of the `config/param_FCCee/hh.py`
3. Then create appropriate Pythia8 card, by appending standard card with decay syntax if needed and add it to the proper directory.
For a given production tag <prodtag> of FCC-ee this directory is:

```shell
/eos/experiment/fcc/ee/generation/FCC-config/<prodtag>/FCCee/Generator/Pythia8/
```

:::{admonition} Nota Bene
:class: callout

Please do not write directly on EOS. Cards should be added by making a
documented pull request to the corresponding production tag branch in
[FCC-config](https://github.com/HEP-FCC/FCC-config/).
:::

4. Send the jobs:

```shell
python bin/run.py --FCChh/FCCee --reco --send --type lhep8 --condor -p <process> -N <njobs> -q <queue> --prodtag <prodtag> --detector <detector>
```

Example produce 10 jobs of FCC Delphes events of ttz decaying the Z to neutrinos. :

```shell
python bin/run.py --FCCee --reco --send --type lhep8 --condor -p mg_ee_zhh_ecm365 -N 10 -q workday --prodtag spring2021 --detector IDEA
```

Please note that the decay in pythia is optional, and that there is no need to specify the number of events to run on as it will by default run over all the events present in the LHE file

The options `--ncpus` and `--priority` can also be specified to increase the numbers of cpus on the cluster and to change the priority queue.


## Generate EDM4hep files from STDHEP

To produce Delphes EDM4hep files from STDHEP, just run this kind of command

```shell
python bin/run.py --FCCee --reco --send --type stdhep --condor -p <process> -N <njobs> -q <queue> --prodtag <prodtag> --detector <detector>
```

For example to run over one STDHEP file of mumuH process:

```shell
python bin/run.py --FCCee --reco --send --type stdhep --condor -p wzp6_ee_mumuH_ecm240 -N 1 -q longlunch --prodtag spring2021_training --detector IDEA
```


## Generate EDM4hep files from Pythia8

This section describe the way most of the events were produced, using Pythia directly. The steps to be followed can be described as:
1. Define process in `pythialist` in the `config/param_FCCee/hh.py` corresponding to your FCC choice.
2. Write Pythia8 process card and put it in: `/eos/experiment/fcc/ee/generation/FCC-config/<prodtag>/FCCee/Generator/Pythia8` by making a Pull Request to the corresponding production tag branch of [FCC-config](https://github.com/HEP-FCC/FCC-config/) for example `p8_ee_Zbb_ecm91.cmd`
3. Once the Pull Request is approved and the file has appeared on the corresponding `<prodtag>` on `eos`, send jobs

```shell
python bin/run.py --FCC-hh/FCCee --reco --send --type p8 --condor -p <process>  --pycard <pythia_card> -n <nevents> -N <njobs> -q <queue> --prodtag <prodtag> --detector <detector>
```

Example produce 1 job of 10000 events of ZH at FCC-ee 240GeV

```shell
python bin/run.py --FCCee --reco --send --type p8 -p p8_ee_ZH_ecm240 -n 10000 -N 1 --condor -q longlunch --prodtag spring2021 --detector IDEA
```

The options `--ncpus` and `--priority` can also be specified to increase the numbers of cpus on the cluster and to change the priority queue.

:::{admonition} Important
:class: callout

If `--pycard` option is not specified, this step will run with the default
Pythia8 card (in this case `p8_ee_default.cmd`), that does not include specific
decays nor specific matching/merging parameters.
:::

To assist you in writing your own Pythia8 configuration cards, the manual is available [here](http://home.thep.lu.se/~torbjorn/pythia81html/Welcome.html)

## Expert mode

The following commands should be run with care, as they update the database, web-page etc...
They run automatically every four hours with crontab, thus you will eventually know when your samples are ready to be used by browsing the corresponding configuration on this [web-page](http://fcc-physics-events.web.cern.ch/).
The `--force` option is used to force the script to run in order to optimize running time, processes that have not been flagged will not be checked.

### Updating the database

1. First one need to check the eos directories that have been populated with new files.

Example for LHE:

```shell
python bin/run.py --FCCee --LHE --checkeos [--process process] [--force]
```

Example for Delphes events:

```shell
python bin/run.py --FCCee --reco --checkeos --prodtag spring2021 [--process process] [--force]
```

2. Second one need to check the quality of the files that have been produced.
Example for LHE:

```shell
python bin/run.py --FCCee --LHE --check [--process process] [--force]
```

Example for Delphes events:

```shell
python bin/run.py --FCCee --reco --check --prodtag spring2021 [--process process] [--force]
```

3. Then the checked files needs to be merged (individual yaml files are created for each file produced and the information needs to be aggregated):
Example for LHE:

```shell
python bin/run.py --FCCee --LHE --merge [--process process] [--force]
```

Example for Delphes events:

```shell
python bin/run.py --FCCee --reco --merge --prodtag spring2021 [--process process] [--force]
```

### Cleaning bad jobs

To clean jobs that are flagged as bad, the following command can be used for LHE:

```shell
python bin/run.py --FCCee --LHE --clean [--process process]
```

and for Delphes

```shell
python bin/run.py --FCCee --reco --clean --prodtag spring2021 [--process process]
```

As the code checks the files that are in the end written on eos, we need to clean also old jobs that don't produced outputs 3 days after they started.
To do so run the following command for LHE

```shell
python bin/run.py --FCCee --LHE --cleanold [--process process]
```

and for Delphes

```shell
python bin/run.py --FCCee --reco --cleanold --prodtag spring2021 [--process process]
```

If you want to completly remove a process, the following command can be used with care for LHE:

```shell
python bin/run.py --FCCee --LHE --remove --process process
```

and for Delphes

```shell
python bin/run.py --FCCee --reco --remove --process process --prodtag spring2021
```


### Update the webpage

The webpage can be updated after the files have been checked and merged by running for LHE

```shell
python bin/run.py --FCCee --LHE --web
```

and for Delphes

```shell
python bin/run.py --FCCee --reco --web --prodtag spring2021
```


### Create the sample list for analyses

To create the list of samples to be used in physics analyses for `spring2021` production tag:

```shell
python bin/run.py --FCCee --reco --sample --prodtag spring2021
```

### All in One

a script can be used to do all the steps in one go, for example for LHE at FCC-ee:

```shell
./scripts/cronrun_LHE_FCCee.sh
```

and for Delphes events:

```shell
./scripts/cronrun_RECO_FCCee.sh <prodtag> <detector>
```

for example for Delphes events with `spring2021` production tag and `IDEA` detector:

```shell
./scripts/cronrun_RECO_FCCee.sh spring2021 IDEA
```

## Produce samples with EventProducer outside of official campaign

This section explains how you can use the EventProducer to produce your own database of events.
1. You first need to create three output directories with sufficient disk space. One where the samples could be written, for example on your CERN `eos`. An other public directory to store the database that is created and associate each job/file on eos, and one that can be browsed from the web, for example using your eos cern box for all:

```shell
For samples  /eos/home-<X>/<cernlogin>/generation/
For public   /eos/home-<X>/<cernlogin>/public/FCCDicts/
For web      /eos/home-<X>/<cernlogin>/www/data/FCCee/
```

2. Edit the file `config/param_FCCee.py`:
    - Replace `webbasedir` by your directory `For web`
    - Replace `pubbasedir` by your directory `For public`
    - Replace `eosbaseoutputdir` by `For samples`
    - If you want to use your own `FCC-config`, also replace `eosbaseinputdir` to point to where it is cloned.

3. You should now be ready to send jobs using your own work areas, you will have to run the checks yourself, have a look at the [Expert mode](#expert-mode)
