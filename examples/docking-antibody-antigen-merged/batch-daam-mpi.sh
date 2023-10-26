#!/bin/bash
#SBATCH --job-name=daam-mpi-batch

job1=docking-antibody-antigen-CDR-accessible-mpi-6.job
job2=docking-antibody-antigen-CDR-accessible-mpi-36.job
job3=docking-antibody-antigen-CDR-accessible-mpi-72.job

job1_name=daam-mpi-6
job2_name=daam-mpi-36
job3_name=daam-mpi-72

job1_id=$(sbatch --job-name="$job1_name" $job1 | awk '{print $NF}')
echo "jobid1: $job1_id"
job2_id=$(sbatch --job-name="$job2_name" --dependency=afterany:$job1_id $job2 | awk '{print $NF}')
echo "jobid2: $job2_id"
sbatch --job-name="$job3_name" --dependency=afterany:$job2_id $job3
