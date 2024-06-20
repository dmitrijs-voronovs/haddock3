#!/bin/bash

rundir=$1
infodir="$rundir.info"
scontrol show nodes > $infodir/nodes_info.after.txt
ps aux > $infodir/proc_info.after.txt
echo "Collecting info for $rundir (after run) done."