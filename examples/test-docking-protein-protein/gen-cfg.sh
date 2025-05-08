
#!/bin/bash/

filename="test-hpc"
cfg_template="template/${filename}-template.cfg"

cfg_template_concat="___CONCAT___"
cfg_template_queue_limit="___QUEUE_LIMIT___"
cfg_template_ntasks="___NTASKS___"
cfg_template_cpus_per_task="___CPUS_PER_TASK___"


# script that accepts ncores, nodes, tasks_per_node as cli arguments and replaces them in template files

# get cli arguments
concat=$1
qlim=$2
ntasks=$3
cpuspt=$4

#create cfg and job files with ncores in filename
cfg_file="${filename}-con${concat}-qlim${qlim}-ntask${ntasks}-cpupt${cpuspt}.cfg"

echo "filename: $job_file, concat: $concat, qlim: $qlim, ntasks: $ntasks, cpuspt: $cpuspt"	

# copy template files
cp $cfg_template $cfg_file

# replace ncores in cfg file
sed -i "s/$cfg_template_concat/$concat/g" $cfg_file
sed -i "s/$cfg_template_queue_limit/$qlim/g" $cfg_file
sed -i "s/$cfg_template_ntasks/$ntasks/g" $cfg_file
sed -i "s/$cfg_template_cpus_per_task/$cpuspt/g" $cfg_file
