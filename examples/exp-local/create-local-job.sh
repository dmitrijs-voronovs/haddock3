#!/bin/bash/

workflow=$1

filename="$workflow-local"
cfg_template="template/${filename}-template.cfg"

cfg_template_ncores="___NCORES___"
cfg_template_node="___NODE___"
cfg_template_trial="___TRIAL___"
cfg_template_run_dir="___RUNDIR___"

# script that accepts ncores, nodes, tasks_per_node as cli arguments and replaces them in template files

# get cli arguments
ncores=$2
node=$3
trial=$4

#create cfg and job files with ncores in filename
concat_args="$filename-nc$ncores-($node-$trial)"
cfg_file="$concat_args.cfg"
run_dir="run.$concat_args"

echo $cfg_template 
echo "filename: $cfg_file, ncores: $ncores, node: $node, trial: $trial, run_dir: $run_dir"

# copy template files
cp "$cfg_template" "$cfg_file"

# replace ncores in cfg file
sed -i "s/$cfg_template_ncores/$ncores/g" $cfg_file
sed -i "s/$cfg_template_node/$node/g" $cfg_file
sed -i "s/$cfg_template_trial/$trial/g" $cfg_file
sed -i "s/$cfg_template_run_dir/$run_dir/g" $cfg_file
