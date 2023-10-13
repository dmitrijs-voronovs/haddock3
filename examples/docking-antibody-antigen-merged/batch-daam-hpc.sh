#!/bin/bash
#SBATCH --job-name=daam-hpc-batch

job1=docking-antibody-antigen-CDR-accessible-hpc-50.cfg
job2=docking-antibody-antigen-CDR-accessible-hpc-100.cfg
job3=docking-antibody-antigen-CDR-accessible-hpc-4949.cfg

job1_name=daap-hpc-50
job2_name=daap-hpc-100
job3_name=daap-hpc-4949

job1_id=$(sbatch --job-name="$job1_name" haddock3 $job1 --restart=0 | awk '{print $NF}')
echo "jobid1: $job1_id"
job2_id=$(sbatch --job-name="$job2_name" --dependency=afterany:$job1_id haddock3 $job2 --restart=0  | awk '{print $NF}')
echo "jobid2: $job2_id"
sbatch --job-name="$job3_name" --dependency=afterany:$job2_id haddock3 $job3 --restart=0
