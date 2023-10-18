#!/bin/bash

file_name="test-hpc-1-4949"
cfg="$file_name.job"
test_type="(ntasks=32)"
data_dir="run.$file_name"

rm -rf $data_dir
sbatch --ntasks 32 --job-name=$file_name-$test_type $cfg