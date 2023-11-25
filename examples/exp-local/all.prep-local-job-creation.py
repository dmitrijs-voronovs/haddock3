def getCreateCommand(workflow, ncores, node, trial, is_warmup=False):
    return f"sh create-local-job.sh {workflow} {ncores} {node} {trial}{' warmup' if is_warmup else ''}"


commands = [
    getCreateCommand(workflow, ncores, node, trial)
    for workflow in ["dpp", "daa"]
    for node in ["gl2", "gl6"]
    for ncores in [2, 4, 8]
    for trial in range(1, 11)
    ] + [
    getCreateCommand(workflow, ncores, node, trial)
    for workflow in ["dpp", "daa"]
    for ncores in [16, 32]
    for node in ["gl6"]
    for trial in range(1, 11)
    ] + [getCreateCommand("dpp", 8, "gl2", 1, True), getCreateCommand("dpp", 8, "gl6", 1, True)]


for command in commands:
    print(command)

with open("all.create-local-job.sh", "w") as file:
    file.writelines("#!/bin/bash/ \n")
    file.writelines("\n".join(commands))
