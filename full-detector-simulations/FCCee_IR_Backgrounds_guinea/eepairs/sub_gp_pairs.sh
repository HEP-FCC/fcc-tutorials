nruns=100

let "j=1"

for i in `seq ${j} ${nruns}`
do

    ROOTDIR=/afs/cern.ch/user/v/voutsina/Work/FCCeeBKG_WrapUp/eepairs
    mkdir $ROOTDIR/data${i}
    cd $ROOTDIR/data${i}

    cd $ROOTDIR/data${i}
    #echo directory
    #echo $ROOTDIR
    nn=${i}*100000
    echo $nn

    cp $ROOTDIR/acc.dat .
    sed -i -e 's/rndm_seed=100000/rndm_seed='${nn}'/g' acc.dat

    cat > test_sub.sh << EOF1
#!/bin/sh
cp $ROOTDIR/data${i}/acc.dat .
/afs/cern.ch/user/v/voutsina/Work/testarea/CodeTest/GP++/guinea-pig.r3238/src/guinea FCCee_Top FCCee_Top output
mv pairs.dat $ROOTDIR/data${i}
mv pairs0.dat $ROOTDIR/data${i}
mv output $ROOTDIR/data${i}
EOF1

    chmod u+x test_sub.sh

    cat > paok.sub << EOF1
    executable            =  test_sub.sh
    log                   =$ROOTDIR/data${i}/logfile.log
    output                =$ROOTDIR/data${i}/STDOUT 
    error                 =$ROOTDIR/data${i}/STDERR
+JobFlavour = "tomorrow"
queue 1
EOF1

    chmod u+x paok.sub

    condor_submit paok.sub

done