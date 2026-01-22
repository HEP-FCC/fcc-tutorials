# Overview of the job submission script

>
> Original author: Gerardo Ganis
>

Command line user submission to DIRAC WMS (Workload Management System) is
performed using Python scripts instantiating the relevant classes. The general
structure of the script is following:

1. Instantiation of the interface to the iLCDirac;
2. Creation of a Job manager instance, including input and output sandbox, and
   all relevant configuration and data files;
3. Creation and configuration of the application(s) to be run and their
   registration to the job manager instance;
4. Job submission

The script may contain or import all the code relevant to the correct
definition of the various steps above. DIRAC also provides some standard
tooling for parsing arguments to homogenize the submission script experience.

The parser is defined in the DIRAC core, is part of the generic definition of
[Script][script] and provides a callback for customizing the actions. Typical
usage looks like this:

```python
from DIRAC import S_OK, gLogger
from DIRAC.Core.Base import Script

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


def main():
    # Instantiate the params class
    cli_params = Params()

    # Register simple on/off switches
    Script.registerSwitch('w', 'wms', 'Run on DIRAC WMS',
                          cli_params.run_on_wms)
    Script.registerSwitch('l', 'local', 'Run locally',
                          cli_params.run_locally)

    # Parse the command line and initialize DIRAC
    Script.parseCommandLine()

    # The result of the command line parsing is stored in the params class
    gLogger.notice('cli_params.where: ', cli_params.where)


if __name__ == '__main__':
    main()
```

The DIRAC interface is controlled by the API interface class `DiracILC`, which
derives from the upstream [DIRAC API][diracapi]. Typical usage is the following:

```python
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

...

dilc = DiracILC()
```

The returned `dILc` variable contains the API context to be used when relevant.

The job manager is an instance of `UserJob` - which derives from [Job][job]
&mdash; is instantiated next. Typical usage is the following:

```python
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob

...

job = UserJob()
job.setOutputSandbox(['*.log', '*.sh', '*.py', '*.xml'])
outputdatafile='kktautau_delphes_edm4hep_output.root'
job.setOutputData(outputdatafile, '', 'CERN-DST-EOS')
job.setJobGroup('KKMC_EDM4HEP_Run')
job.setName('KKMC_EDM4HEP')
job.setLogLevel('DEBUG')

...

# Information can be added through out the script 
delphescard = 'delphes_card_IDEA.tcl'

...

# Set the sandbox content
job.setInputSandbox(['./' + delphescard, './' + edm4hepoutdef, './' + pythiacard])
```

Applications are created, configured and added to the job manager in the order
of running. An example is the following:

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

Available applications can be found [here][diracapp].

Finally the job is submitted with:

```python
print job.submit(dilc, mode='wms')
# Use wms='local' for running on the local computer
```

Local submission can be used for testing.

## Before starting: cloning of workflows repository

The example scripts described in these pages, together with the relevant setup
scripts, are available from the [FCCDIRAC][fccdirac] repository.

The following steps have to be executed before trying to execute any
of the example workflows:

1. Clone the FCCDIRAC repository and enter the `workflows` directory within the
   repository
   ```bash
   git clone https://github.com/HEP-FCC/FCCDIRAC
   cd FCCDIRAC/workflows
   ```

2. Setup the iLCDirac/DIRAC environment
   ```bash
   source setup_dirac.sh
   ```
   The expected output:
   ```
   Setting the iLCDirac environment ...
   ```

3. Setup the GRID user proxy
   ```bash
   source setup_proxy.sh
   ```
   The expected output:
   ```
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

[script]: https://dirac.readthedocs.io/en/latest/CodeDocumentation/Core/Base/Script.html
[diracapi]: https://github.com/DIRACGrid/DIRAC/blob/integration/src/DIRAC/Interfaces/API/Dirac.py
[job]: https://dirac.readthedocs.io/en/latest/UserGuide/GettingStarted/UserJobs/
[diracapp]: https://gitlab.cern.ch/CLICdp/iLCDirac/ILCDIRAC/-/tree/Rel-v35r0/src/ILCDIRAC/Interfaces/API/NewInterface/Applications
[fccdirac]: https://github.com/HEP-FCC/FCCDIRAC
