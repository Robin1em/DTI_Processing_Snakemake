#!/bin/bash

# Define the parent directory containing the sub-directories
parent_dir="/storage/biomeds/projects/neurorad-drg-dti/data/New_Data_2024_07_08_edited/BIPN"

# Function to run Snakemake in a directory
run_snakemake() {
    local dir="$1"
    echo "Running Snakemake in $dir"
    # Navigate to the directory
    cd "$dir" || return
    # Run Snakemake with parallel execution in a detached mode
    nohup snakemake --cores 2 -p --executor slurm --jobs 10 --default-resources mem_mb=1000 cpus_per_task=2 --snakefile /storage/biomeds/projects/neurorad-drg-dti/snakemake_code/DTI_snakemake.smk --configfile /storage/biomeds/projects/neurorad-drg-dti/snakemake_code/config.yml --latency-wait 1000 > "${dir}/snakemake.log" 2>&1 &
    # Note: Redirect stdout and stderr to snakemake.log in the working directory
    # Return to the parent directory after processing
    cd ..
}

# Iterate over each sub-directory
for dir in "$parent_dir"/*; do
    if [ -d "$dir" ]; then
        # Run Snakemake in the background
        run_snakemake "$dir"
    fi
done
