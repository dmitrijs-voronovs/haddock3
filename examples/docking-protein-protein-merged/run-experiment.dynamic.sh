#!/bin/bash

# Create an array of job names
jobs=(
    "docking-protein-protein-local-2-gl5.cfg"
    "docking-protein-protein-local-2-GreenLab-STF.cfg"
    "docking-protein-protein-local-4-gl5.cfg"
    "docking-protein-protein-local-4-GreenLab-STF.cfg"
    "docking-protein-protein-local-8-gl5.cfg"
    "docking-protein-protein-local-8-GreenLab-STF.cfg"
    "docking-protein-protein-local-32-gl5.cfg"
    "docking-protein-protein-local-16-gl5.cfg"
)

# Get a random order of the jobs
random_order=$(shuf -i 0-7 -n 8)

# Create a new script with the jobs in the random order
cat > check-jobs-local.sh << EOF
#!/bin/bash
for job in "${jobs[@]:$random_order}"
do
    job_id=\$(sbatch --job-name="\${job}" --nodelist=\${nodelist} --dependency=afterany:\${dependency} haddock3 \${job} | awk '{print \$NF}')
    dependency="\${dependency}:\${job_id}"
done
EOF
```