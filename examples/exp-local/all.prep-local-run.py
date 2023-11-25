import random
from typing import List


class Config:
    def __init__(self, workflow, ncores, node, trial, is_warmup=False):
        self.workflow = workflow
        self.ncores = ncores
        self.node = node
        self.trial = trial
        self.name = f"{workflow}-local-nc{ncores}_{node}-{trial}.{'warmup.' if is_warmup else ''}cfg"

    @property
    def runDir(self):
        return f"run.{self.name}"


def create_experiment_job(nodes: List[str], experiment_name: str):
    def get_list_intersection(list1, list2):
        return list(set(list1) & set(list2))

    configs = [
        Config(workflow, ncores, node, trial)
        for workflow in ["dpp", "daa"]
        for node in get_list_intersection(["gl2", "gl6"], nodes)
        for ncores in [2, 4, 8]
        for trial in range(1, 11)
        ] + [
        Config(workflow, ncores, node, trial)
        for workflow in ["dpp", "daa"]
        for ncores in [16, 32]
        for node in get_list_intersection(["gl6"], nodes)
        for trial in range(1, 11)
        ]

    random.shuffle(configs)

    warmup_config = Config("dpp", 8, nodes[0], 1, True)

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
cat > check-{experiment_name}.sh << EOF
#!/bin/bash
echo {job_ids}
sacct -o jobid,jobname%50,cluster,Node,state,start,end,ConsumedEnergy,AveRSS,AveDiskRead,AveDiskWrite,AveVMSize,elapsed,NCPUS \
    -j {job_ids} \
    > {experiment_name}-data.txt
cat {experiment_name}-data.txt
EOF
'''

    with open(f"run-{experiment_name}.sh", "w", newline='\n') as file:
        file.write("#!/bin/bash/ \n")
        file.write("\n".join(commands))
        file.write(check_jobs_sh.format(
            job_ids=job_ids, experiment_name=experiment_name))


create_experiment_job(["gl2"], "local-exp-gl2")
create_experiment_job(["gl6"], "local-exp-gl6")
