## Overview of the submission scripts

Command line submission to DIRAC is performed using python scripts instantiating the relevant classes.
The general structure of the script is the following:

1. Instantiation of the interface to DIRAC;
2. Creation of a Job manager instance, including input and output sandbox, and all relevant config and data files; 
3. Creation and configuration of the application to be run and their registration to the job manager instance;
4. Job submission

The script may contain or import all the code relevant to the correct definition of the various steps above.
DIRAC also provides some standard tooling for parsing arguments and homogenize the submission script experience. 

The parser is defined the DIRAC core, is part of the generic definition of [Script][script] and provides a callback for
customizing the actions. Typical usage looks like this:

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
# The value for argument 'wms' is the first entry in servicelist list

```

[script]: https://dirac.readthedocs.io/en/latest/CodeDocumentation/Core/Base/Script.html

The DIRAC interface is controlled by the API interface class `DiracILC`, which derives from the upstream [DIRAC API][diracapi].
Typical usage is the following:

```python
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
...
dIlc = DiracILC()
```

The returned `dILc` variable contais the API context to be used when relevant.

[diracapi]: https://raw.githubusercontent.com/DIRACGrid/DIRAC/integration/src/DIRAC/Interfaces/API/Dirac.py

The job manager is an instance of `UserJob` - which derives from [Job][job] - is instantiated next.
Typical usage is the following:

```python
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
...
job = UserJob()
job.setOutputSandbox(['*.log', '*.sh', '*.py', '*.xml'])
outputdatafile='kktautau_delphes_edm4hep_output.root'
job.setOutputData(outputdatafile, '','CERN-DST-EOS' )
job.setJobGroup( "KKMC_EDM4HEP_Run" )
job.setName( "KKMC_EDM4HEP" )
job.setLogLevel("DEBUG")
...
# Information can be added thorugh out the script 
delphescard='delphes_card_IDEA.tcl'
...
# Set the sandbox content
job.setInputSandbox(['./' + delphescard, './' + edm4hepoutdef, './' + pythiacard])
```

[job]: https://dirac.readthedocs.io/en/latest/UserGuide/GettingStarted/UserJobs/

Applications are created, configured and added to the job manager in the order of running:
An example is the following:

```python
from ILCDIRAC.Interfaces.API.NewInterface.Applications import KKMC
...
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

Available applications defined in [here][diracapp].

[diracapp]: https://gitlab.cern.ch/CLICdp/iLCDirac/ILCDIRAC/-/tree/Rel-v31r0/Interfaces/API/NewInterface

Finally the job is submitted:

```python
print job.submit(dIlc, mode='wms')
# Use wms='local' for running on the local computer
```

Local submission can be used for testing.

### Before starting: cloning of workflows repository

The example scripts described in these pages, together with the relevant setup scripts, are available from the
[FCCDIRAC][fccdirac] repository.

The following steps must be executed (only once!) before trying to execute any of the workflows:

```bash
$ git clone https://github.com/HEP-FCC/FCCDIRAC
$ cd FCCDIRAC

$ source init_fcc.sh
Setting up the latest Key4HEP software stack from CVMFS ...
 ...  Key4HEP release: key4hep-stack/2021-07-16
 ... Use the following command to reproduce the current environment:
 ...
         source /cvmfs/sw.hsf.org/spackages2/key4hep-stack/2021-07-16/x86_64-centos7-gcc8.3.0-opt/wxwfgu65rjnk7s6frj25qsoq5miay4ft/setup.sh
 ...
 ... done.

$ source init_dirac.sh
Setting the iLCDirac environment ...

$ source init_dirac_proxy.sh
Initializing the DIRAC/Grid proxy ...
Generating proxy...
Enter Certificate password:
Added VOMS attribute /fcc
Uploading proxy..
Proxy generated:
subject      : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis/CN=2888907760/CN=1791020771
issuer       : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis/CN=2888907760
identity     : /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis
timeleft     : 23:53:59
DIRAC group  : fcc_user
path         : /tmp/x509up_u2759
username     : ganis
properties   : NormalUser
VOMS         : True
VOMS fqan    : ['/fcc']

Proxies uploaded:
 DN                                                                           | Group | Until (GMT)
 /DC=ch/DC=cern/OU=Organic Units/OU=Users/CN=ganis/CN=393971/CN=Gerardo Ganis |  | 2022/05/13 12:12
```

[fccdirac]: https://github.com/HEP-FCC/FCCDIRAC
