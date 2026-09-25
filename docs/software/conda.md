---
title: "Conda on Phoebe"
description: "Get conda from the Miniforge3 module and use it in interactive shells and batch jobs"
tags:
  - "conda"
  - "python"
---

# Conda on Phoebe

!!! warning "TODO"
    Confirm that the `Miniforge3` module is the recommended way to get conda on Phoebe, and
    whether `/etc/profile.d/conda.sh` (used in the [CosmoSIS guide](cosmosis-py27.md)) is
    still supported or should be removed from that guide.

## Activate conda

Load the Miniforge3 module and initialise conda for the current shell:

```
module load Miniforge3
source ${EBROOTMINIFORGE3}/etc/profile.d/conda.sh
```

This does not modify your `~/.bashrc`, so conda is only active in this shell. Use the same two
lines at the start of batch job scripts.

!!! warning "TODO"
    Add the recommended Miniforge3 version (`module spider Miniforge3`) if users should pin one.

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
