# Workflow 1: Ditau with KKMCee + Delphes

>
> Original author: Gerardo Ganis
>

:::{admonition} Purpose
:class: objectives

Demonstrate the use of DIRAC to generate 10'000 $\tau^{+}\tau^{-}$ events
@ $91.2~\mathrm{GeV}$ with KKMC and pass them through the IDEA detector with the
help of Delphes framework.
:::

## Location of the output files

The placement of the job output files depends on where the job runs.

**Local mode**  
The output file is located under a sub-directory name `Local_<hash>_JobDir`
created under the current directory.

**DIRAC WMS mode**  
In WMS mode the file will be located under

```
<chosen-storage-element>/fcc/user/<first-username-letter>/<username>/<year>_<month>/<first-5-numbers-of-jobID>/<jobID>/edm4hep_test_output.root
```

e.g. at CERN (storage element `CERN-DST-EOS`):

```
/eos/experiment/fcc/prod/fcc/user/g/ganis/2021_07/59821/59821752/edm4hep_test_output.root
```


## DIRAC components involved

This exercise consists of two steps, the event generation with [KKMCee][kkmcee]
and afterwards the simulation of the detector response with [Delphes][delphes].

For the first step we need the [KKMC DIRAC application][kkmc-dirac-app] which
we configure with the process, the number of events, the energy and the name of
the output file.

The second step consists of running the standalone `DelphesPythia8_EDM4HEP`
executable from the Key4hep stack as an
[DIRAC Generic Application][generic-dirac-app] while manually passing all the
needed arguments:

1. The `Delphes` card implementing the IDEA detector concept;
2. The definition of the EDM4hep output;
3. The Pythia card reading LHE file formats;
4. The output file.

For this we use the generic application DIRAC interface.

## The workflow script, dissected

The submission script for this workflow is called
[FCC_Dirac_Workflow1.py][workflow1-py]. The script accepts only one argument to
control where the job is executed:

```bash
python FCC_Dirac_Workflow1.py -h
```

```
Usage:
  FCC-Dirac-Workflow1 [options] ...

General options:
  -o  --option <value>         : Option=value to add
  -s  --section <value>        : Set base section for relative parsed options
  -c  --cert <value>           : Use server certificate to connect to Core Services
  -d  --debug                  : Set debug mode (-ddd is extra debug)
  -   --cfg=                   : Load additional config file
  -   --autoreload             : Automatically restart if there's any change in the module
  -   --license                : Show DIRAC's LICENSE
  -h  --help                   : Shows this help

Options:
  -w  --wms                    : Run on DIRAC WMS
  -l  --local                  : Run locally
```


### Helper copy function

In order to ease the preparation of the job input files a helper function, which
aids with string replacements is defined at the top of the script.

```python
def copywithreplace(filein: str, fileout: str,
                    repls: list[tuple[str, str]] = []):
    '''
    Copy the contents of the file with possible string replacements.
    '''
    # If no replacements, just copy the file
    if repls is None:
        copy2(filein, fileout)
        return

    # Load the contents of the input file
    with open(filein, 'rt', encoding='utf-8') as infile:
        # open the output file to write the result to
        lines = infile.readlines()
    with open(fileout, 'wt', encoding='utf-8') as outfile:
        # for each line in the input file
        for line in lines:
            # Apply each requested replacement
            lout = line
            for rpl in repls:
                lout = lout.replace(str(rpl[0]), str(rpl[1]))
            outfile.write(lout)
```


### Adding the `--wms` switch

As described in the [](../Overview.md) we define a simple switch to have
command line control over where the job will be executed.

```python
from DIRAC import gLogger, S_OK
from DIRAC.Core.Base import Script

...

# Define a simple class to hold the script parameters
class Params:
    def __init__(self):
        self.where = 'local'
    def run_on_wms(self, _):
        self.where = 'wms'
        return S_OK()
    def run_locally(self, _):
        self.where = 'local'
        return S_OK()

...

    # Setup argument parsing
    cli_params = Params()

    Script.registerSwitch('w', 'wms', 'Run on DIRAC WMS',
                          cli_params.run_on_wms)
    Script.registerSwitch('l', 'local', 'Run locally',
                          cli_params.run_locally)

    Script.parseCommandLine()
```


### The DIRAC Job manager

```python
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob

...

job = UserJob()
job.setOutputSandbox(['*.log', '*.sh', '*.py', '*.xml'])
outputdatafile='kktautau_delphes_edm4hep_output.root'
job.setOutputData(outputdatafile, '', 'CERN-DST-EOS' )

job.setJobGroup("KKMC_EDM4HEP_Run")
job.setName("KKMC_EDM4HEP")
job.setLogLevel("DEBUG")
```

### The `KKMC` application instance

The [KKMC DIRAC application][kkmc-dirac-app] requires a few settings.

```python
from ILCDIRAC.Interfaces.API.NewInterface import Applications

...

    kkmc_app = Applications.KKMC()
    kkmc_app.setVersion('key4hep_250128')
    kkmc_app.setEvtType('Tau')
    kkmc_app.setEnergy(91.2)
    nevts = 10000
    outputfile = f'kktautau_delphes_{nevts}.lhe'
    kkmc_app.setNumberOfEvents(nevts)
    kkmc_app.setOutputFile(outputfile)

    # Register KKMC application to the Job instance
    job.append(kkmc_app)
```


### Preparing the `Delphes` input cards

First, all the needed input cards need to be prepared in the submission
directory. In this example workflow the cards are provided alongside the
submission script and are copied (and adjusted) to the submission directory.

```python
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Delphes IDEA card
    # copy of $DELPHES/cards/delphes_card_IDEA.tcl
    idea_card = 'delphes_card_IDEA.tcl'
    copy2(os.path.join(script_dir, idea_card), idea_card)
    # Delphes EDM4hep output card
    # copy of $K4SIMDELPHES/edm4hep_output_config.tcl
    edm4hep_output_def = 'edm4hep_output_config.tcl'
    copy2(os.path.join(script_dir, edm4hep_output_def), edm4hep_output_def)
    # Pythia card
    # copy of $K4GEN/Pythia_LHEinput.cmd
    pythia_card = 'Pythia_LHEinput.cmd'
    replacements = [
        ('Main:numberOfEvents = 100',
         f'Main:numberOfEvents = {nevts}'),
        ('Beams:LHEF = Generation/data/events.lhe',
         f'Beams:LHEF = {outputfile}')
    ]
    copywithreplace(os.path.join(script_dir, pythia_card), pythia_card,
                    replacements)
```


### Completing the sandbox for `Delphes`

In order for the job to be able to pick up our input cards we need to register
them for the input sandbox.

```python
    # Set the sandbox content
    job.setInputSandbox(
        ['./' + idea_card, './' + edm4hep_output_def, './' + pythia_card]
    )
```

### Standalone `Delphes` using the generic DIRAC application

```python
from ILCDIRAC.Interfaces.API.NewInterface import Applications

...

    ga = Applications.GenericApplication()
    ga.setSetupScript(
        '/cvmfs/sw.hsf.org/key4hep/releases/2025-01-28/'
        'x86_64-almalinux9-gcc14.2.0-opt/key4hep-stack/'
        '2025-01-28-q6hyek/setup.sh'
    )
    ga.setScript(
        '/cvmfs/sw.hsf.org/key4hep/releases/2025-01-28/'
        'x86_64-almalinux9-gcc14.2.0-opt/k4simdelphes/00-07-04-naw5vm/'
        'bin/DelphesPythia8_EDM4HEP'
    )
    ga.setArguments(
        f'{idea_card} {edm4hep_output_def} {pythia_card} {outputdatafile}'
    )

    job.append(ga)
```


### Submitting the job

```python
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

...

    dilc = DiracILC()
    print(job.submit(dilc, mode=cli_params.where))
```


## Running the job submission script

After having cloned the repository and initialized the environment, go to the
workflow sub-directory, create a submission directory `run` and launch the
submission script from there:

```bash
cd workflow/1
mkdir run; cd run
```

### Local submission

Run the submission script with the `--local` switch

```bash
python ../FCC_Dirac_Workflow1.py --local
```

The summary of the job will be printed for the inspection, afterwards confirm or
decline the submission. The whole output should look similar to this:

```
Submitting Example Workflow 1
 - execution location:  local
kkmc key4hep_250128
Attribute list :
  ...
  version: key4hep_250128
  steeringFile: Not defined
  inputFile: Not defined
  outputFile: kktautau_delphes_10000.lhe
  ...
  logFile: kkmc_key4hep_250128_Step_1.log
  ...
  numberOfEvents: 10000
  energy: 91.2
  ...
  _extension: hepmc


ApplicationScript
Attribute list :
  script: /cvmfs/sw.hsf.org/key4hep/releases/2025-01-28/x86_64-almalinux9-gcc14.2.0-opt/k4simdelphes/00-07-04-naw5vm/bin/DelphesPythia8_EDM4HEP
  setupScript: /cvmfs/sw.hsf.org/key4hep/releases/2025-01-28/x86_64-almalinux9-gcc14.2.0-opt/key4hep-stack/2025-01-28-q6hyek/setup.sh
  arguments: delphes_card_IDEA.tcl edm4hep_output_config.tcl Pythia_LHEinput.cmd kktautau_delphes_edm4hep_output.root
  ...
  logFile: ApplicationScript_Step_2.log
  ...
  energy: 91.2
  ...


Proceed and submit job(s)? y/[n] : y

...
<very long output>
...

2026-01-20 09:29:32 UTC dirac-jobexec DEBUG: Workflow execution successful, exiting
Standard output written to std.out
{'OK': True, 'Value': 'Execution completed successfully'}
```

After the execution the submission directory should contain the following files:

```bash
ls -lt
```

```
total 44
drwx------. 3 jsmiesko jsmiesko  4096 Jan 20 13:31 Local_dp5xm4kz_JobDir
-rw-r--r--. 1 jsmiesko jsmiesko  1483 Jan 20 13:30 Pythia_LHEinput.cmd
-rw-r--r--. 1 jsmiesko jsmiesko   580 Jan 20 09:49 edm4hep_output_config.tcl
-rw-r--r--. 1 jsmiesko jsmiesko 30239 Jan 20 09:49 delphes_card_IDEA.tcl
```

in this example workflow it should contain the input cards and the local output
directory:

```bash
ls -lt Local_dp5xm4kz_JobDir/
```
```txt
total 39712
-rw-r--r--. 1 jsmiesko jsmiesko        1 Jan 20 13:31 std.err
-rw-r--r--. 1 jsmiesko jsmiesko        1 Jan 20 13:31 std.out
-rw-r--r--. 1 jsmiesko jsmiesko    32268 Jan 20 13:31 ApplicationScript_Step_2.log
-rw-r--r--. 1 jsmiesko jsmiesko   135662 Jan 20 13:31 kktautau_delphes_edm4hep_output.root
-rw-r--r--. 1 jsmiesko jsmiesko   318074 Jan 20 13:30 localEnv.log
-rw-r--r--. 1 jsmiesko jsmiesko   176236 Jan 20 13:30 kkmc_key4hep_250128_Step_1.log
-rw-r--r--. 1 jsmiesko jsmiesko 19609219 Jan 20 13:30 events.hepmc
drwxr-xr-x. 2 jsmiesko jsmiesko      146 Jan 20 13:30 KKMCee-20Jan2026-130159
-rw-r--r--. 1 jsmiesko jsmiesko 19609219 Jan 20 13:30 kktautau_delphes_10000.lhe
-rwxr-xr-x. 1 jsmiesko jsmiesko      613 Jan 20 13:30 kkmc_key4hep_250128_Run_1.sh
-rwxr-xr-x. 1 jsmiesko jsmiesko   446528 Jan 20 13:30 DelphesPythia8_EDM4HEP
-rw-r--r--. 1 jsmiesko jsmiesko   154244 Jan 20 13:30 setup.sh
-rw-r--r--. 1 jsmiesko jsmiesko      580 Jan 20 13:30 edm4hep_output_config.tcl
-rw-r--r--. 1 jsmiesko jsmiesko     1483 Jan 20 13:30 Pythia_LHEinput.cmd
-rw-r--r--. 1 jsmiesko jsmiesko    30239 Jan 20 13:30 delphes_card_IDEA.tcl
-rw-r--r--. 1 jsmiesko jsmiesko    18882 Jan 20 13:30 jobDescription.xml
```


### DIRAC WMS submission

Run the submission script with the `--wms` switch
```bash
python ../FCC_Dirac_Workflow1.py --wms
```

The initial output will be similar to the local mode, but after confirming the
submission you should get JSON dump which should contain the job ID.
```
...
Proceed and submit job(s)? y/[n] :
y
...
{'OK': True, 'Value': 66251838, 'JobID': 66251838, ...
```

#### Monitoring the submitted job

The `JobID` defines uniquely the job and can be used, for example, to check the
status of the job with `dirac-wms-job-status`:

```bash
dirac-wms-job-status 66251838
```

```txt
JobID=66251838 ApplicationStatus=Unknown; MinorStatus=Pilot Agent Submission; Status=Waiting; Site=ANY;
```

To more closely monitor the execution of the job one can also use
`dirac-wms-job-logging-info`:

```bash
dirac-wms-job-logging-info 66251838
```
```txt
Source            Status         MinorStatus             ApplicationStatus  DateTime
=================================================================================================
JobManager        Received       Job accepted            Unknown            2026-01-20 10:31:01
JobPath           Checking       JobSanity               Unknown            2026-01-20 10:31:01
JobSanity         Checking       SoftwareVersions        Unknown            2026-01-20 10:31:01
SoftwareVersions  SoftwareCheck  Done                    Unknown            2026-01-20 10:31:01
SoftwareVersions  Checking       JobScheduling           Unknown            2026-01-20 10:31:01
JobScheduling     Waiting        Pilot Agent Submission  Unknown            2026-01-20 10:31:02
...
...
```

#### Retrieving job output

When the job is finished, one can get the job output files (includes job
description, log files, application scripts, ...):

```bash
dirac-wms-job-get-output 66251838
```

```txt
Files retrieved and extracted in /home/jsmiesko/dirac-workflows/FCCDIRAC/workflows/1/run2/66251838
Job output sandbox retrieved in /home/jsmiesko/dirac-workflows/FCCDIRAC/workflows/1/run2/66251838/
```

```bash
ls -lt 66251838/
```

```
total 832
-rw-r--r--. 1 jsmiesko jsmiesko 109703 Jan 20 11:37 std.out
-rw-r--r--. 1 jsmiesko jsmiesko  26159 Jan 20 11:37 std.err
-rw-r--r--. 1 jsmiesko jsmiesko  32382 Jan 20 11:37 ApplicationScript_Step_2.log
-rw-r--r--. 1 jsmiesko jsmiesko 311550 Jan 20 11:37 localEnv.log
-rw-r--r--. 1 jsmiesko jsmiesko 183261 Jan 20 11:37 kkmc_key4hep_250128_Step_1.log
-rwxr-xr-x. 1 jsmiesko jsmiesko    620 Jan 20 11:37 kkmc_key4hep_250128_Run_1.sh
-rw-r--r--. 1 jsmiesko jsmiesko 154244 Jan 28  2025 setup.sh
-rw-r--r--. 1 jsmiesko jsmiesko  18882 Jan  1  1970 jobDescription.xml
```

#### Accessing the job results

The files with the job results (ROOT files, LHE files, ...) can be retrieved
using the `dirac-wms-job-get-output-data`:

```bash
dirac-wms-job-get-output-data 66251838
```

```txt
Attempting to retrieve /fcc/user/j/jsmiesko/2026_01/66251/66251838/kktautau_delphes_edm4hep_output.root
Trying to download root://x509up_u1000@eospublic.cern.ch//eos/experiment/fcc/prod/fcc/user/j/jsmiesko/2026_01/66251/66251838/kktautau_delphes_edm4hep_output.root to /home/jsmiesko/dirac-workflows/FCCDIRAC/workflows/1/run2/kktautau_delphes_edm4hep_output.root
Job 66251838 output data retrieved
```

Now the resulting root file should be located in your local directory:
```bash
ls -lt kktautau_delphes_edm4hep_output.root
```

```txt
-rw-r--r--. 1 jsmiesko jsmiesko 135662 Jan 20 13:52 kktautau_delphes_edm4hep_output.root
```

Since this example workflow defines `CERN-DST-EOS` Storage Element as its
output data location, we can also access the resulting file through EOS at CERN:
```bash
ls -lt /eos/experiment/fcc/prod/fcc/user/j/jsmiesko/2026_01/66251/66251838/
```

```txt
total 133
-rw-r--r--. 1 140035 2855 135662 Jan 20 11:37 kktautau_delphes_edm4hep_output.root
```

#### Listing jobs of the user

The listing of the jobs of the user can be retrieved with the
`dirac-wms-select-jobs` command, e.g.

```
dirac-wms-select-jobs --Date=2021-07-28 --Owner="ganis"
```

```
==> Selected 1 jobs with conditions: Date = 2021-07-28, Owner = ganis
59838136
```

All possible selection options can be listed by providing `--help` argument
```txt
dirac-wms-select-jobs --help

Select DIRAC jobs matching the given conditions


Usage:
  dirac-wms-select-jobs [options] ...

General options:
  -o  --option <value>         : Option=value to add
  -s  --section <value>        : Set base section for relative parsed options
  -c  --cert <value>           : Use server certificate to connect to Core Services
  -d  --debug                  : Set debug mode (-ddd is extra debug)
  -   --cfg=                   : Load additional config file
  -   --autoreload             : Automatically restart if there's any change in the module
  -   --license                : Show DIRAC's LICENSE
  -h  --help                   : Shows this help

Options:
  -   --Status=                : Primary status
  -   --MinorStatus=           : Secondary status
  -   --ApplicationStatus=     : Application status
  -   --Site=                  : Execution site
  -   --Owner=                 : Owner (DIRAC nickname)
  -   --JobGroup=              : Select jobs for specified job group
  -   --Date=                  : Date in YYYY-MM-DD format, if not specified default is today
  -   --Maximum=               : Maximum number of jobs shown (default 100, 0 means all)
```

Another possibility is to use the [iLCDirac web portal][diracweb].

[delphes]: https://delphes.github.io/
[kkmcee]: https://kkmcee.docs.cern.ch/
[kkmc-dirac-app]: https://gitlab.cern.ch/CLICdp/iLCDirac/ILCDIRAC/-/blob/Rel-v35r0/src/ILCDIRAC/Interfaces/API/NewInterface/Applications/KKMC.py
[generic-dirac-app]: https://gitlab.cern.ch/CLICdp/iLCDirac/ILCDIRAC/-/blob/Rel-v35r0/src/ILCDIRAC/Interfaces/API/NewInterface/Applications/GenericApplication.py
[workflow1-py]: https://raw.githubusercontent.com/HEP-FCC/FCCDIRAC/master/workflows/1/FCC_Dirac_Workflow1.py
[diracweb]: https://voilcdiracwebapp2.cern.ch/DIRAC/?theme=Classic&url_state=1|*DIRAC.JobMonitor.classes.JobMonitor:,
