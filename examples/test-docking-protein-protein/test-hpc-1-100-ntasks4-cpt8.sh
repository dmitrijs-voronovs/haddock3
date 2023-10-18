#!/bin/bash

file_name="test-hpc-1-100"
cfg="$file_name.job"
test_type="(ntasks=4,cpus-per-task=8)"
data_dir="run.$file_name"

rm -rf $data_dir
sbatch --ntasks 4 --cpus-per-task 8 --job-name=$file_name-$test_type $cfg