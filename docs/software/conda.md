---
title: "Conda on Phoebe"
description: "Get conda from the Miniforge3 module and use it in interactive shells and batch jobs"
tags:
  - "conda"
  - "python"
---

# Conda on Phoebe

Conda comes from the `Miniforge3` module in the `system` stack, on the login node and on all
compute nodes. There is no system-wide conda installation (`/etc/profile.d/conda.sh` does not
exist).

## Activate conda

Load the Miniforge3 module and initialise conda for the current shell:

```
module load Miniforge3
source ${EBROOTMINIFORGE3}/etc/profile.d/conda.sh
```

This does not modify your `~/.bashrc`, so conda is only active in this shell. Use the same two
lines at the start of batch job scripts.

Three versions are installed: `Miniforge3/24.7.1-2`, `25.3.1-0` and `26.3.2-3`. Without a
version, `module load Miniforge3` picks the newest. Name a version in job scripts, for example
`module load Miniforge3/26.3.2-3`, so that a new default doesn't change your environment.

## Create and use an environment

```
conda create --name myenv python=3.12
conda activate myenv
```

Where to store environments:

!!! warning "TODO"
    Say where environments and the package cache should live (home quota, a project or
    scratch directory) and how to set `envs_dirs` / `pkgs_dirs` in `~/.condarc` if home is
    too small.

## In a batch job

```
#!/bin/bash
#SBATCH --job-name=conda-example
#SBATCH --partition=cpu
#SBATCH --ntasks=1

module load Miniforge3
source ${EBROOTMINIFORGE3}/etc/profile.d/conda.sh
conda activate myenv

python my_script.py
```

## Guides that use conda

* [CuPy on GPUs](cupy.md)
* [Pyoperon](pyoperon.md)
* [CosmoSIS with Python 2.7](cosmosis-py27.md)
