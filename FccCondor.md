[]() Getting Started with HTCondor CLI
======================================

Contents:

-   [HTCondor CLI](#htcondor-cli)
    -   [Overview](#overview)
    -   [Submission](#submission)
        -   [1- The submit file](#1-submit-file)
        -   [2- Changing the job's requirements](#2-job-req)
        -   [3- Changing the job's software](#3-job-soft)
   -   [Testing](#testing)
   -   [Perspective](#perspective)


[]() Overview
-------------

HTCondor is a management system for job submission. It has been chosen as the successor of LSF at CERN.

As for LSF, you have to log in to an lxplus machine with your cern account if you want to access to the batch.


[]() Submission
---------------

Instead of passing the job and its requirements as arguments to the command as you
usually do with bsub, you just have to pass a submit file :

	condor_q job.sub

If you are bored to understand how it works you can directly play with HTcondor [here !](#testing) otherwise, please continue.

### []() 1- The submit file

First of all you have to write a submit file i.e **job.sub** as an example with the following content :

	executable            = tmpjob.sh

	arguments             = $(ClusterID) $(ProcId)

	output                = output/job.$(ClusterId).$(ProcId).out

	log                   = log/job.$(ClusterId).log

	error                 = error/job.$(ClusterId).$(ProcId).err

	send_credential        = True

	queue


where we have the following attributes :

- executable is the path of your job
- arguments are the arguments of your job
- output contains the path of the standard output of your job
- error contains the path of the standard error of your job


### []() 2- Changing the job's requirements

We provide you a simple submit file but generally, we have more complex stuff to do.
So if you want to know more about attributes like the number of job you want etc...
Please take a look at these webpages :


[Cern's Tutorial](http://batchdocs.web.cern.ch/batchdocs/local/quick.html)

[Wisconsin's Tutorial](http://research.cs.wisc.edu/htcondor/tutorials/intl-grid-school-3/submit_first.html)

### []() 3- Changing the job's software

For this example we choose to use an intermediate job **tmpjob.sh** instead of the job directly for the "executable".

The reason why we do this is because we have to source a script setting the environement variables which is [init_fcc_stack.sh](https://github.com/HEP-FCC/fcc-spi/blob/master/init_fcc_stack.sh)

This script is essential if you are using FCC softwares because it contains the paths of all installed software your job may need.

As the job you submitted is running on a remote machine you have to source the script on the executing remote machine and which you don't have access.

That's why we have an intermediate script **tmpjob.sh** that we can consider as an intermediate job, hence the name "tmp". This script "initialize" the fcc stack on the remote machine.

Here is the content of **tmpjob.sh** :



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


where we have the following variables :

- fcc_input_file is the path of your input file

- fcc_software is the path of your software

In this basic example :

- the fcc_software is "fcc-pythia8-generate"
- the input_file is "ee_ZH_Zmumu_Hbb.txt"

After, the script calls the executable (software) followed by the input file.

By Default, the results should appear in the current working directory.


[]() Testing
-------------


Login to an lxplus machine and ensure that you have kerberos tickets, as this will authenticate you and your job. Run kinit to refresh tokens as necessary.

After, type the following commands (you can just copy and past on a shell and type enter) :

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

By Default, the results "ee_ZH_Zmumu_Hbb.root" should appear in the current working directory.

You can check the status of your job by typing :

	condor_q


[]() Perspective
----------------

We are working on accessing to HTCondor from an high level interface to make life easier for end-users than with command line.

We plan to use an existing Python Binding to access HTCondor and offer you a 'nice' GUI.




For more informations please contact me at : sabri.fernana@gmail.com 
