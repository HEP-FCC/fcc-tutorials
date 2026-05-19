import math
import random
import os

theFile = open("/afs/cern.ch/user/v/voutsina/Work/SR/data_gen/FCC_TTPLS_BND_18JUL_TA_M38_5MI_INC_TRKS_BOT.DAT") # all impinging photons to the mask
#theFile = open("/afs/cern.ch/user/v/voutsina/Work/SR/data_gen/FCC_TTPLS_BND_18JUL_TA_M38_250MI_ALL_TRKS.DAT") # all scattered photons from 1 beam & 1 mask
#theFile = open("/afs/cern.ch/user/v/voutsina/Work/SR/data_gen/FCC_TTPLS_BND_18JUL_TA_M38_1BI_TRKS.DAT") # forward scattered photons from 1 beam & 1 mask

j = -1

#MeV = 1e-3	# Mike's energies are in MeV, convert to GeV

MeV = 1		# when we run ddsim via enableGun and the ddg4 commands, the energy is passed in MeV, not in GeV...
cm  = 10  	#  Mike's positions in cm, convert to mm

ijob = 0
Nev = 1 #10 BX
#Nev =  12 #3.4872      # 5# Nb of events to run for each line in Mike's file #100 m bend
#Nev = 169	# Nb of events to run for each line in Mike's file #42 m bend
Nlines = 5000000    # Nb of lines to be processed per job

k = 0           # counter that is reset when Nlines lines have been read

NJOBMAX=-1	# set NJOBMAX=-1 for full prod, NJOBMAX = e.g. 3 or 4 for a test

#NJOBMAX=2
#HalfCrossingAngle = 15./1000.   #  15 mrad
#CosTheta = math.cos( HalfCrossingAngle )
#SinTheta = math.sin( HalfCrossingAngle )

def submit( steeringFile, subjobFile, ijob ) :
           steeringFile.close()
           outputFile.close()
           aa="echo exit >>"+steeringFile.name
           os.system(aa)
           execFile.write("#!/bin/sh" + "\n")
           execFile.write("source /cvmfs/clicdp.cern.ch/iLCSoft/builds/2019-04-17/x86_64-slc6-gcc7-opt/init_ilcsoft.sh" + "\n")
           execFile.write("DETFILE=/afs/cern.ch/work/v/voutsina/guineapig++/guinea-pig.r3238/data/PairsZ/BeamParTest/Pairs/Geometry/FCCee_o1_v04/FCCee_o1_v04.xml" + "\n")
           execFile.write("cp /afs/cern.ch/user/v/voutsina/Work/SR/Scripts/"+steeringFile.name +" ./. \n")
           #execFile.write("ddsim --compactFile $DETFILE --physics.rangecut 50e-3 --numberOfEvents 35 --outputFile=" +outputFile.name+ " --steeringFile=" + steeringFile.name+ "\n" )
           execFile.write("ddsim --compactFile $DETFILE  --outputFile=" +outputFile.name+ " --enableGun --physics.rangecut 50e-3 --runType shell < " + steeringFile.name  +  " > lo \n")
	   #execFile.write("mv dummyOutput.slcio /afs/cern.ch/user/v/voutsina/Work/SR/Scripts/Results/ddsim_"+str(ijob)+".slcio" + "\n")
	   execFile.write("mv " +outputFile.name+ " /afs/cern.ch/user/v/voutsina/Work/SR/Scripts/Results/Simulation/ALL_INCIDENT_PHOTONS" + "\n")
           execFile.close()

           subjobFile.write("executable = "+execFile.name +"\n")
           subjobFile.write("log = /afs/cern.ch/user/v/voutsina/Work/SR/Scripts/Output/logfile.log \n")
           subjobFile.write("output = /afs/cern.ch/user/v/voutsina/Work/SR/Scripts/Output/STDOUT \n")
           subjobFile.write("error = /afs/cern.ch/user/v/voutsina/Work/SR/Scripts/Output/STDERR \n")
           subjobFile.write("+JobFlavour =\"workday\" \n")
           subjobFile.write("queue 1\n")
         #  subjobFile.write("cp /afs/cern.ch/user/a/akolano/private/SIMULATIONS/NEW_GEO_FIX/hits_sim.xml  hits_sim.xml  \n")
         #  subjobFile.write("sed -e \"s@HACKRUNNUMBER@"+str(ijob)+"@g\" lctuple_simhits_digi_Oct27.xml > lctuple_simhits_digi.xml \n")
         #  subjobFile.write("Marlin --global.LCIOInputFiles=dummyOutput.slcio hits_sim.xml   > lo2  \n")
         #  subjobFile.write("eos cp blah.root /eos/fcc/user/a/akolano/SynchRad/NEW_GEO_BX/lctuple_"+str(ijob)+".root \n")
           subjobFile.close()

           os.system("chmod 777 "+subjobFile.name )
           os.system("chmod 777 "+execFile.name )
          # os.system("bsub -q 1nd "+subjobFile.name )
          # os.system("bsub -q 1nd "+subjobFile.name )
           os.system("condor_submit " +subjobFile.name )


if __name__ == '__main__':


  for fl in theFile :

	if NJOBMAX>0 and ijob > NJOBMAX:
	    break

        if j < 0 :  # skip header line
           j=j+1
           continue

	if k == 0:
	   ijob = ijob + 1

	   outputFile = open("output_"+str(ijob)+".slcio","w")
	   steeringFile = open("steering_"+str(ijob)+".py","w")
	   steeringFile.write("/ddg4/Gun/Particle gamma \n")
           #steeringFile.write("SIM.gun.particle = \"gamma\"  \n")
	   print "created steering for ijob =",ijob

	   execFile = open("exec_"+str(ijob)+".sh","w")
	   subjobFile = open("sub_"+str(ijob),"w")
	   #os.system(" cp subbase.tmp sub_"+str(ijob) )
	   
	   #os.system("cat  subbase.tmp > " +execFile.name )
	   subjobFile.close()
	   subjobFile = open("sub_"+str(ijob),"a")


        j = j +1
	k = k + 1



############################
	thesplit = fl.split()
	energy = float(thesplit[0]) 
        energy = energy * MeV          # I assume that the energy is in MeV in Mike's file

        cosalpha_p = float(thesplit[4] )
        cosbeta = float( thesplit[5] )
        cosgamma_p = float( thesplit[6] )

	vx = float(thesplit[1] ) * cm
	#vx = -23.0 original Mikes, had different cord sys 
        vy = float( thesplit[2]) * cm
        vz = float( thesplit[3] ) * cm
################################################
        #px_prime = energy * cosalpha_p
        #pz_prime = energy * cosgamma_p

        #pz = CosTheta * pz_prime - SinTheta * px_prime
        #px = SinTheta * pz_prime + CosTheta * px_prime

        #cosalpha = px / energy
        #cosgamma = pz / energy

        p = str(energy)

	steeringFile.write("/ddg4/Gun/energy "+p + " \n")
        steeringFile.write("/ddg4/Gun/direction ("+str(cosalpha_p)+", "+str(cosbeta)+", "+str(cosgamma_p)+") \n" )
	steeringFile.write("/ddg4/Gun/Position ("+str(vx)+", "+str(vy)+", "+str(vz)+") \n" )
	steeringFile.write("/run/beamOn "+str(Nev) + "\n")


	if k ==Nlines:
	   submit( steeringFile, subjobFile, ijob )
	   k = 0

  if k > 0 :   # the last job was not submitted because less than NLines 
	submit( steeringFile, subjobFile, ijob )


 
