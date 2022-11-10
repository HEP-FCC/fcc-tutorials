# Production of events

The production of events for FCC physics studies is done using the [EventProducer](https://github.com/HEP-FCC/EventProducer) framework.
In order to use it, please get in contact with the FCC software and computing coordinators as running central production of events specific rights [(see here)](https://hep-fcc.github.io/FCCSW/computing/computing.html). When samples produced by this framework they will appear on this [web-page](http://fcc-physics-events.web.cern.ch/)


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
python bin/run.py --FCCee --LHE --send --condor --typelhe <gp> -p <process> -n <nevents> -N <njobs> -q <queue> --prodtag <prodtag> --detector <detector>
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

**N.B.** At the moment no example is generated for FCC-ee this way. Below is an example for FCC-hh.

As before, you need to add the process to the `config/param_FCChh.py` file. Then you can run with the following command:

```shell
python bin/run.py --FCC --LHE --send --condor --typelhe mg -p mg_pp_hh_test --mg5card mg5/examples/pp_hh.mg5 --model mg5/models/loop_sm_hh.tar -N 2 -n 10000 -q workday  --memory 16000. --disk 8000.
```

The options `--ncpus` and `--priority` can also be specified to increase the numbers of cpus on the cluster and to change the priority queue.



## Generate FCCSW files from the LHE and decay with Pyhtia8

1. If you want to let Pythia decay without specifying anything, you can use the default card, but if you have requested extra partons at matrix element, you might need to specify matching parameters to your pythia card
2. If you want to use a specific decay, make sure that the decay you want is in `decaylist` and `branching_ratios` of the `config/param_FCCee/hh.py`
3. Then create appropriate Pythia8 card, by appending standard card with decay syntax if needed and add it to the proper directory.
For a given production tag <prodtag> of FCC-ee this directory is:

```shell
/eos/experiment/fcc/ee/generation/FCC-config/<prodtag>/FCCee/Generator/Pythia8/
```

**N.B.**: please do not write directly on eos. Cards should be added by making a documented pull request to the corresponding production tag branch in [FCC-config](https://github.com/HEP-FCC/FCC-config/)

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


## Generate FCCSW files from Pythia8

This section describe the way most of the events were produced, using Pythia directly. The steps to be followed can be described as:
1. Define process in pythialist in the `config/param_FCCee/hh.py` corresponding to your FCC choice.
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

**Important**: If `--pycard` option not specified, this step will run with the default Pythia8 card (in this case `p8_ee_default.cmd`), that does not include specific decays nor specific matching/merging parameters.

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

a script can be used
