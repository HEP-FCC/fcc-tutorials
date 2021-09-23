# Workflow 1

## Purpose

Demonstrate the use of DIRAC generate 10000 tau+tau- events @91.2 GeV with KKMC and process through Delphes/IDEA.

## Output files

**Local mode**<br>
The output file is located under a sub-directory name `Local_<hash>_JobDir` created under the current directory.

**WMS mode**<br>
In WMS mode the file will be located under

```
<chosen-storage-element>/fcc/user/<first-username-letter>/<username>/<year>_<month>/<first-5-numbers-of-jobID>/<jobID>/edm4hep_test_output.root
```

e.g. at CERN (storage element `CERN-DST-EOS`):

```
/eos/experiment/fcc/prod/fcc/user/g/ganis/2021_07/59821/59821752/edm4hep_test_output.root
```

## DIRAC components involved

This exercise constist of two steps, the event generation with `KKMCee` and the `Delphes` simulation.

For the first step we need the `KKMC` DIRAC application which we configure with the process, the number of events, the energy and
the nale of the output file.

The second step consists in running the `DelphesPythia8_EDM4HEP` standalone application with arguments

1. The `Delphes` card implementing the IDEA detector concept;
2. The definition of the EDM4hep output;
3. The pythia card reading LHE file formats;
4. The output file.

For this we use the generic application DIRAC interface.

## The script, dissected

The submission script for this workflow is called [FCC_Dirac_Workflow1.py][workflow1-py].
The script accepts one argument to control where the job is executed:

```
python FCC_Dirac_Workflow1.py -h
```

```

Usage:

  FCC_Dirac_Workflow1.py (<options>|<cfgFile>)*

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
  -w  --wms                    : WMS where to run
```

[workflow1-py]: https://raw.githubusercontent.com/HEP-FCC/FCCDIRAC/master/workflows/1/FCC_Dirac_Workflow1.py

### The utility function

```python
# Create sandbox files
import os
from shutil import copy2
import array

# Utility function
def copywithreplace(filein, fileout, repls):
    # If no replacements, just copy the file
    if len(repls) == 0:
        copy2(filein, fileout)
        return
    # input file
    fin = open(filein, "rt")
    # output file to write the result to
    fout = open(fileout, "wt")
    # for each line in the input file
    for line in fin:
        # Apply each requested replacement
        ltmp = line
        for r in repls:
            lout = ltmp.replace(str(r[0]), str(r[1]))
            ltmp = lout
        fout.write(lout)
    # close input and output files
    fin.close()
    fout.close()
```

### Adding the `--wms` switch

```python
from DIRAC import S_OK, S_ERROR
from DIRAC.Core.Base import Script

# Define a simple class to hold the script parameters
class Params(object):
  def __init__(self):
    self.wms = 'wms'
  def setWMS(self, value):
    self.wms = value
    return S_OK()

# Instantiate the params class
cliParams = Params()
Script.registerSwitch('w', 'wms', "WMS where to run", cliParams.setWMS)
Script.parseCommandLine(ignoreErrors=False)
# Get the list of services (the switch above appearer as servicesList[0])
servicesList = Script.getPositionalArgs()
print servicesList
```

### The DIRAC API instance

```python
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

dIlc = DiracILC()
```

### The DIRAC Job manager

```python
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob

job = UserJob()
job.setOutputSandbox(['*.log', '*.sh', '*.py', '*.xml'])
outputdatafile='kktautau_delphes_edm4hep_output.root'
job.setOutputData(outputdatafile, '','CERN-DST-EOS' )

job.setJobGroup( "KKMC_EDM4HEP_Run" )
job.setName( "KKMC_EDM4HEP" )
job.setLogLevel("DEBUG")
```

### The `KKMC` application instance

```python
from ILCDIRAC.Interfaces.API.NewInterface.Applications import KKMC

kkmc = KKMC()
kkmc.setVersion('Key4hep-2021-04-30')
kkmc.setEvtType('Tau')
kkmc.setEnergy(91.2)
nevts = 10000
outputfile = 'kktautau_delphes_' + str(nevts) + '.LHE'
kkmc.setNumberOfEvents(nevts)
kkmc.setOutputFile(outputfile)

job.append(kkmc)
```

### The steering files for `Delphes`

```python
# Delphes card
delphescardpath=os.path.expandvars('$DELPHES/cards/delphes_card_IDEA.tcl')
delphescard=os.path.basename(delphescardpath)
copy2(delphescardpath, delphescard)
# EDM4hep output definition
edm4hepoutdefpath=os.path.expandvars('$K4SIMDELPHES/edm4hep_output_config.tcl')
edm4hepoutdef=os.path.basename(edm4hepoutdefpath)
copy2(edm4hepoutdefpath, edm4hepoutdef)
# Pythia card
pythiacardpath=os.path.expandvars('$K4GEN/Pythia_LHEinput.cmd')
pythiacard=os.path.basename(pythiacardpath)
replacements = [['Main:numberOfEvents = 100','Main:numberOfEvents = ' + str(nevts)],
                ['Beams:LHEF = Generation/data/events.lhe','Beams:LHEF = ' + outputfile]]
copywithreplace(pythiacardpath, pythiacard, replacements)
```

### Completing the sandbox for `Delphes`

```python
# Set the sandbox content
job.setInputSandbox(['./' + delphescard, './' + edm4hepoutdef, './' + pythiacard])
```

### Standalone `Delphes` using the DIRAC generic application 

```python
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GenericApplication

ga = GenericApplication()
ga.setSetupScript("/cvmfs/sw.hsf.org/spackages2/key4hep-stack/2021-04-30/x86_64-centos7-gcc8.3.0-opt/t5gcd6ltt2ikybap2ndoztsg5uyorxzg/setup.sh")
ga.setScript("/cvmfs/sw.hsf.org/spackages2/k4simdelphes/00-01-05/x86_64-centos7-gcc8.3.0-opt/beesqo4r5wuqrrijyz57kxbqcdp5pp4v/bin/DelphesPythia8_EDM4HEP")
ga.setArguments(delphescard + ' ' + edm4hepoutdef + ' ' + pythiacard + ' ' + outputdatafile)

job.append(ga)
```

### Submitting the job to the chosen WMS

```python
submitmode='wms'
if len(servicesList) > 0:
    submitmode= servicesList[0]
print job.submit(dIlc, mode=submitmode)
```

## Running the script on lxplus

Suggestion is, after having cloned the repository and initialized the environment, to go to the workflow sub-directory, created a 'run' sub-directory and run
from there:

```
$ cd workflow/1
$ mkdir run; cd run
```

### Local submission

```bash
$ python ../FCC_Dirac_Workflow1.py --wms local
```

```
['local']
kkmc Key4hep-2021-04-30
Attribute list :
  forgetAboutInput: Not defined
  randomSeed: -1
  outputSE: Not defined
  seedFile: Not defined
  energy: 91.2
  ...
  logFile: kkmc_Key4hep-2021-04-30_Step_1.log

ApplicationScript
Attribute list :
  forgetAboutInput: Not defined
  outputSE: Not defined
  energy: 91.2
  ...
  logFile: ApplicationScript_Step_2.log


Proceed and submit job(s)? y/[n] : y

[long output]

2021-07-28 16:27:53 UTC dirac-jobexec/ILCDIRAC.Workflow.Modules.UserJobFinalization INFO: GUID = CCADDA80-3B2E-7E9C-3C14-5A493AB48BD4
2021-07-28 16:27:53 UTC dirac-jobexec DEBUG: Workflow execution successful, exiting
{'OK': True, 'Value': 'Execution completed successfully'}
```

The local sandbox should contain the following:

```
$ ls -lt
```
```
total 32
drwx------. 2 ganis sf  2048 Jul 28 18:27 Local_pQl06k_JobDir
-rw-r--r--. 1 ganis sf  1483 Jul 28 18:25 Pythia_LHEinput.cmd
-rw-r--r--. 1 ganis sf   587 May 10 15:31 edm4hep_output_config.tcl
-rw-r--r--. 1 ganis sf 27219 Apr 30 14:50 delphes_card_IDEA.tcl
```

and the output directory:

```
$ ls -lt Local_pQl06k_JobDir/kktautau*
-rw-r--r--. 1 ganis sf  9642099 Jul 28 18:27 Local_pQl06k_JobDir/kktautau_delphes_edm4hep_output.root
-rw-r--r--. 1 ganis sf 32586567 Jul 28 18:27 Local_pQl06k_JobDir/kktautau_delphes_10000.LHE
$ ls -lt Local_pQl06k_JobDir/*.log
-rw-r--r--. 1 ganis sf 257109 Jul 28 18:27 Local_pQl06k_JobDir/ApplicationScript_Step_2.log
-rw-r--r--. 1 ganis sf  44250 Jul 28 18:27 Local_pQl06k_JobDir/kkmc_Key4hep-2021-04-30_Step_1.log
-rw-r--r--. 1 ganis sf 900532 Jul 28 18:27 Local_pQl06k_JobDir/localEnv.log
```

### WMS submission

```bash
python ../FCC_Dirac_Workflow1.py
```

```
...
Proceed and submit job(s)? y/[n] :
y
...
'Value': 59838136, 'JobID': 59838136}
```

The `JobID` defines uniquely the job and can be used for any operation, for example to check the status:

```
dirac-wms-job-status 59838136
```

```
JobID=59838136 Status=Waiting; MinorStatus=Pilot Agent Submission; Site=ANY;
```

or, when the job is finished,  get the job files:

```
$ dirac-wms-job-get-output 59838136
```
```
Job output sandbox retrieved in /afs/cern.ch/user/g/ganis/local/dirac/GIT/FCCDIRAC/workflows/1/run/59838136/
$ ls -lt 59838136/
total 1295
-rw-r--r--. 1 ganis sf 273338 Jul 28 19:13 std.out
-rw-r--r--. 1 ganis sf  38583 Jul 28 19:13 std.err
-rw-r--r--. 1 ganis sf 256445 Jul 28 19:13 ApplicationScript_Step_2.log
-rw-r--r--. 1 ganis sf 464310 Jul 28 19:12 localEnv.log
-rw-r--r--. 1 ganis sf  43690 Jul 28 19:12 kkmc_Key4hep-2021-04-30_Step_1.log
-rwxr-xr-x. 1 ganis sf    559 Jul 28 19:12 kkmc_Key4hep-2021-04-30_Run_1.sh
-rw-r--r--. 1 ganis sf 227185 Apr 30 15:47 setup.sh
-rw-r--r--. 1 ganis sf  19080 Jan  1  1970 jobDescription.xml
```
or get the output data:

```
$ dirac-wms-job-get-output-data 59838136
```

```
Job 59838136 output data retrieved
$ ls -lt kktautau_delphes_edm4hep_output.root
-rwxr-xr-x. 1 ganis sf 9652641 Jul 29 11:30 kktautau_delphes_edm4hep_output.root
```

The output data are also available on storage element:

```
$ ls -lt /eos/experiment/fcc/prod/fcc/user/g/ganis/2021_07/59838/59838136/
```
```
total 9427
-rw-r--r--. 1 fcc001 fcc-cg 9652641 Jul 28 19:13 kktautau_delphes_edm4hep_output.root
```

The job id of the user jobs get also be retrieved with the `dirac-wms-select-jobs` command, e.g.
```
$ dirac-wms-select-jobs --Date=2021-07-28 --Owner="ganis"
```
```
==> Selected 1 jobs with conditions: Date = 2021-07-28, Owner = ganis
59838136
```
or from the web portal.

