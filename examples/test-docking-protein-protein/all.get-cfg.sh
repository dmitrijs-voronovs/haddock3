#!/bin/bash

config_file="cfg.data.txt"

# Skip the first line
sed 1d "$config_file" | while IFS=$'\t' read -r concat qlim ntasks cpuspt
do
    # Launch create-mpi-job.sh with the arguments
    bash gen-cfg.sh "$concat" "$qlim" "$ntasks" "$cpuspt"
done