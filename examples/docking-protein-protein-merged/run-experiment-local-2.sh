#!/bin/bash

job1=docking-protein-protein-local-2.cfg
job2=docking-protein-protein-local-4.cfg

job1_id=$(sbatch --job-name="$job1" --nodelist=gl6                                haddock3 $job1 | awk '{print $NF}')
job2_id=$(sbatch --job-name="$job2" --nodelist=gl6 --dependency=afterany:$job1_id haddock3 $job2 | awk '{print $NF}')

cat > check-jobs-local-2.sh << EOF
#!/bin/bash
sacct -o jobid,jobname%50,cluster,Node,state,start,end,elapsed,MaxRSS,AveRSS,ConsumedEnergy,AveDiskRead,AveDiskWrite,AveVMSize,NCPUS \
    -j $job1_id,$job2_id \
    > experiment-data-local-2.txt
cp experiment-data-local-2.txt ~/haddock3/data/
EOF