# Getting Started with HTCondor CLI


Contents:

  * [HTCondor CLI](#htcondor-cli)
    * [1 - Overview](#1---overview)
    * [2 - Submission](#2---submission)
      * [a - The submit file](#a---the-submit-file)
      * [b - Changing the job requirements](#b---changing-the-job-requirements)
      * [c - How to run fcc-physics scripts](#c---how-to-run-fcc-physics-scripts)
    * [3 - Testing](#3---testing)
    * [4 - Perspective](#4---perspective)


## 1 - Overview


HTCondor is a management system for job submission. It has been chosen as the successor of LSF at CERN.

As for LSF, you have to log in to an lxplus machine with your cern account if you want to access to the batch.


## 2 - Submission


Instead of passing the job and its requirements as arguments to the command as you
usually do with bsub, you just have to pass a submit file :

```
condor_q job.sub

```

If you are interested to understand how it works you can directly play with HTcondor [here !](#3---testing) otherwise, please continue.

### a - The submit file

First of all you have to write a submit file i.e **job.sub** as an example with the following content :

```

executable            = tmpjob.sh

arguments             = $(ClusterID) $(ProcId)

output                = output/job.$(ClusterId).$(ProcId).out

log                   = log/job.$(ClusterId).log

error                 = error/job.$(ClusterId).$(ProcId).err

send_credential        = True

queue

```

where we have the following attributes :

- executable is the full path and name of the executable you want to launch
- arguments are the arguments of your job
- output contains the path of the standard output of your job
- error contains the path of the standard error of your job


### b - Changing the job requirements

We provide you a simple submit file but generally, you will want to add more options to your file.

For example you can tell HTcondor to run 2 times your job by putting the NUMBER_OF_RUNS_YOU_WANT after queue attribute in the last line of the submit file like this :


```
queue NUMBER_OF_RUNS_YOU_WANT

```

You can even run your job with different input and output directories, so if you want to know more about attributes, please take a look at these webpages :


[Cern's Tutorial](http://batchdocs.web.cern.ch/batchdocs/local/quick.html)

[Wisconsin's Tutorial basic](http://research.cs.wisc.edu/htcondor/tutorials/intl-grid-school-3/submit_first.html)

[Wisconsin's Tutorial advanced](https://research.cs.wisc.edu/htcondor/manual/current/2_5Submitting_Job.html)

### c - How to run fcc-physics scripts

For this example we choose to use an intermediate bash script **tmpjob.sh** that executes the actual script we want to launch for the "executable".

The reason why we do this is because we have to source a script setting the environement variables which is [init_fcc_stack.sh](https://github.com/HEP-FCC/fcc-spi/blob/master/init_fcc_stack.sh)

This script is essential if you are using FCC softwares because it contains the paths of all installed software your job may need.

As the job you submitted is running on a remote machine you have to source the script on the executing remote machine and which you don't have access.

That's why we have an intermediate script **tmpjob.sh** that we can consider as an intermediate job, hence the name "tmp". This script "initialize" the fcc stack on the remote machine.

Here is the content of **tmpjob.sh** :

```

#!/bin/bash

#path of the software
SOFTWARE_PATH_AFS="/afs/cern.ch/exp/fcc/sw/0.7"


#source the script
source $SOFTWARE_PATH_AFS/init_fcc_stack.sh

#your input file
fcc_input_file=$SOFTWARE_PATH_AFS/"fcc-physics/0.1/x86_64-slc6-gcc49-opt/share/ee_ZH_Zmumu_Hbb.txt"

#your software
fcc_software="fcc-pythia8-generate"

#let's go
$fcc_software $fcc_input_file

```

where we have the following variables :

- fcc_input_file is the path of your input file

- fcc_software is the path of your software

In this basic example :

- the fcc_software is "fcc-pythia8-generate"
- the input_file is "ee_ZH_Zmumu_Hbb.txt"

After, the script calls the executable followed by the input file.

By Default, the results should appear in the current working directory.


## 3 - Testing



Login to an lxplus machine and ensure that you have kerberos tickets, as this will authenticate you and your job. Run kinit to refresh tokens as necessary.

After, type the following commands (you can just copy and past on a shell and type enter) :

```

mkdir test
cd test
mkdir error log output 

subfile='
executable            = tmpjob.sh\n
arguments             = $(ClusterID) $(ProcId)\n
output                = output/job.$(ClusterId).$(ProcId).out\n
log                   = log/job.$(ClusterId).log\n
error                 = error/job.$(ClusterId).$(ProcId).err\n
send_credential        = True\n
queue'

echo -e $subfile > "job.sub"

jobfile='
#!/bin/bash\n
#path of the software\n
SOFTWARE_PATH_AFS="/afs/cern.ch/exp/fcc/sw/0.7"\n
#source the script\n
source $SOFTWARE_PATH_AFS/init_fcc_stack.sh\n
#your input file\n
fcc_input_file=$SOFTWARE_PATH_AFS/"fcc-physics/0.1/x86_64-slc6-gcc49-opt/share/ee_ZH_Zmumu_Hbb.txt"\n
#your software\n
fcc_software="fcc-pythia8-generate"\n
#lets go\n
$fcc_software $fcc_input_file'

echo -e $jobfile > "tmpjob.sh"	

chmod 755 "tmpjob.sh"

condor_submit job.sub

```

By Default, the results "ee_ZH_Zmumu_Hbb.root" should appear in the current working directory.


Congratulations !!!

You ran FCC softwares on HTCondor.


You can check the status of your job by typing :

```

condor_q

```

## 4 - Perspective


A High-level interface to make life easier for end-users is available here :

[FCCBATCH](https://github.com/sfernana/fcc-spi/tree/master/batch)
 

For the moment, we are accessing HTCondor from the command line interface but we plan to access it from Python when the python binding will be released.



For any questions or any further informations, please contact us at : fcc-experiments-sw-devATSPAMNOTcern.ch
