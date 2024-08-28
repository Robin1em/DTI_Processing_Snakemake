# Overview

Automated processing pipeline for DTI (Diffusion Tensor Imaging) data, specifically for images of DRG (Dorsal Root Ganglia)

## What does this pipeline do?
- [ ] ROIs are extracted from the images, using fslroi (the parameters can be set in config.yml)
- [ ] The original NIfTI files are split into single volumes and then remergd into two new files (One with all volumes recorded in AP direction with b-values in spending order and one with all b0 volumes, in both AP and PA direction); 
- [ ] For datasets with multiple consecutive volumes with the same bvec entries, these volumes are shortened to one and their temporal mean is calculated
- [ ] The content of the bvec and bval files is rearranged in new files to match the new NIfTI files
- [ ] Config files for popup and eddy are created
- [ ] Then topup and eddy are applied
- [ ] A folder for DTIFit is created and copied for BEDPOSTX (they need the same input data, but different folders)
- [ ] BEDPOSTX and DTIFit are executed

The workflow can be run with SLURM in several directories simultaneously and takes about eight to ten hours to finish.


# Conda environment

The conda environment described in this tutorial can be used to run the workflow:  https://snakemake.readthedocs.io/en/stable/tutorial/tutorial.html


# Which of the two Snakemake files should you use?

There are two slightly different Snakemake workflows: 
- [ ] One workflow for datasets with one or more NIfTI files recorded in AP direction with different b-values, interspersed with b0 volumes and one NIfTI file in PA direction containing only b0 volumes and the corresponding bvec, bval and json files
- [ ] One workflow for datasets with one NIfTI file in AP and one NIfTI file in PA direction with different b-values, interspersed with b0 volumes and the corresponding bvec, bval and json files; these datasets don’t contain separate b0 NIfTI files

For the former, use the DTI_Snakemake.smk workflow and the „ROI_params“ section in config.yml for the fslroi operation; For the latter, use the DTI_Snakemake_old_prot.smk workflow and the „ROI_old“ section in config.yml.


# Config.yml

The configuration file config.yml allows you to set the path to the directory that contains all additional python scripts that are used in the workflow, as well as the parameters for fslroi (separately for both Snakefiles) and the max runtime for each SLURM job. 


# How to run the workflow

You can either navigate into the directory in which your raw data is located and then run the following command (Note that the directory needs a sub-directory called „origs“ that contains the raw data):
snakemake --cores 2  -p --snakefile /path/to/snakefile --configfile /path/to/config.yml --latency-wait 1000 

Or with SLURM: 
snakemake --cores 2  -p --executor slurm --jobs 10 --default-resources mem_mb=1000 cpus_per_task=2 --snakefile /path/to/snakefile --configfile /path/to/config.yml --latency-wait 1000 

Alterantively, if you have multiple directories in which you want to run the workflow, you can use the script „run_snakemake_in_multiple_dirs.sh“. In this script, you need to replace the default paths with the paths to your data, your snakefile and your config.yml file. The bash script needs to be open the whole time while the workflow is running (I know, that’s a bit inconvenient, sorry), so to prevent interruptions, it’s best to run it in a tmux or screen session.
