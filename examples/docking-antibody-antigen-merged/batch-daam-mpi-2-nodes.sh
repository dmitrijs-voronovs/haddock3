#!/bin/bash
#SBATCH --job-name=daam-mpi-batch-2-nodes

job1=docking-antibody-antigen-CDR-accessible-mpi-4.job
job2=docking-antibody-antigen-CDR-accessible-mpi-32.job
job3=docking-antibody-antigen-CDR-accessible-mpi-64.job

job1_name=daam-mpi-4
job2_name=daam-mpi-32
job3_name=daam-mpi-64

job1_id=$(sbatch --job-name="$job1_name" $job1 --restart=0 | awk '{print $NF}')
echo "jobid1: $job1_id"
job2_id=$(sbatch --job-name="$job2_name" --dependency=afterany:$job1_id $job2 --restart=0  | awk '{print $NF}')
echo "jobid2: $job2_id"
sbatch --job-name="$job3_name" --dependency=afterany:$job2_id $job3 --restart=0
