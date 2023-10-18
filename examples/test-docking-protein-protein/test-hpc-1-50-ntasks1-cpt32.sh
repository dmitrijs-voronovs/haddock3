#!/bin/bash

file_name="test-hpc-1-50"
cfg="$file_name.job"
test_type="(ntasks=1,cpus-per-task=32)"
data_dir="run.$file_name"

rm -rf $data_dir

# dependency=$1
# if [ -n "$dependency" ]; then
#     sbatch --dependency=afterany:$dependency --ntasks 1 --cpus-per-task 32 --job-name=$file_name-$test_type $cfg
#     exit 0
# else
    sbatch --ntasks 1 --cpus-per-task 32 --job-name=$file_name-$test_type $cfg
# fi 
