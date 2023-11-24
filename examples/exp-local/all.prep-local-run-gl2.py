import random


class Config:
    def __init__(self, workflow, ncores, node, trial, is_warmup=False):
        self.workflow = workflow
        self.ncores = ncores
        self.node = node
        self.trial = trial
        self.name = f"{workflow}-local-nc{ncores}-({node}-{trial}).{'warmup.' if is_warmup else ''}cfg"

    @property
    def runDir(self):
        return f"run.{self.name}"


configs = [
    Config(workflow, ncores, node, trial)
    for workflow in ["dpp", "daa"]
    for node in ["gl2", "gl6"]
    for ncores in [2, 4, 8]
    for trial in range(1, 11)
    ]


random.shuffle(configs)

warmup_config = Config("dpp", 8, "gl2", 1, True)

commands = [
    f"rm -rf \"run.{warmup_config.name}\"",
    ]

job_idx = -1

configs.insert(0, warmup_config)


for config in configs:
    job_idx += 1
    job_prev_id = f"job{job_idx-1}_2"
    job_check_before_id = f"job{job_idx}_0"
    job_id = f"job{job_idx}_1"
    job_check_after_id = f"job{job_idx}_2"

    dep = f"--dependency=afterany:${job_prev_id}" if job_idx > 0 else ""
    commands.append(
        f"{job_check_before_id}=$(sbatch --job-name=\"info.before.{config.name}\" {dep} collect-info.before.sh \"{config.runDir}\" | awk '{{print $NF}}')")
    commands.append(
        f"{job_id}=$(sbatch --job-name=\"{config.name}\" -n {config.ncores} --dependency=afterany:${job_check_before_id} haddock3 \"{config.name}\" | awk '{{print $NF}}')")
    commands.append(
        f"{job_check_after_id}=$(sbatch --job-name=\"info.after.{config.name}\" --dependency=afterany:${job_id} collect-info.after.sh \"{config.runDir}\" | awk '{{print $NF}}')")

job_ids = ",".join([f"$job{x}_1" for x in range(1, job_idx + 1)])

check_jobs_sh = '''
cat > check-exp-local.sh << EOF
#!/bin/bash
echo {job_ids}
sacct -o jobid,jobname%50,cluster,Node,state,start,end,ConsumedEnergy,AveRSS,AveDiskRead,AveDiskWrite,AveVMSize,elapsed,NCPUS \
    -j {job_ids} \
    > exp-local-data.txt
cat exp-local-data.txt
EOF
'''

with open("run-local-exp.sh", "w") as file:
    file.writelines("#!/bin/bash/ \n")
    file.writelines("\n".join(commands))
    file.writelines(check_jobs_sh.format(job_ids=job_ids))
