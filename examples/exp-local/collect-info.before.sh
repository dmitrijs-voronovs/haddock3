#!/bin/bash

rundir=$1
echo "Coolind down for 5 minutes..."
sleep 300
infodir="$rundir.info"
mkdir $infodir
scontrol show nodes > $infodir/nodes_info.before.txt
ps aux > $infodir/proc_info.before.txt
echo "Collecting info for $rundir (before run) done. Ready to run."