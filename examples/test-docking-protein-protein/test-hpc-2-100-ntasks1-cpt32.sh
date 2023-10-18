#!/bin/bash

file_name="test-hpc-2-100"
cfg="$file_name.job"
test_type="(ntasks=1,cpus-per-task=32)"
data_dir="run.$file_name"

rm -rf $data_dir
sbatch --ntasks 1 --cpus-per-task 32 --job-name=$file_name-$test_type $cfg