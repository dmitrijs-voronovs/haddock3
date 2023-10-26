#!/bin/bash
#SBATCH --job-name=test-job

job1_id=$(sbatch --job-name="test-job-1" test-sleep.sh 10 | awk '{print $NF}')
echo "jobid1: $job1_id"
job2_id=$(sbatch --job-name="test-job-2" --dependency=afterany:$job1_id test-sleep.sh 15  | awk '{print $NF}')
echo "jobid2: $job2_id"
sbatch --job-name="test-job-3" --dependency=afterany:$job2_id test-sleep.sh 5