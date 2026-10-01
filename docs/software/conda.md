---
title: "Conda on Phoebe and Koios"
description: "Get conda from the Miniforge3 module on Phoebe or install it in your home on Koios, and use it in shells and batch jobs"
tags:
  - "conda"
  - "python"
---

# Conda on Phoebe and Koios

On Phoebe, conda comes from the `Miniforge3` module in the `system` stack, on the login node and
on all compute nodes. Use this module rather than installing your own Miniforge or Anaconda. Koios has no Miniforge3 module: install Miniforge3 into your home directory
instead (see [on Koios](#on-koios)). Neither cluster has a system-wide conda installation
(`/etc/profile.d/conda.sh` does not exist).

## On Phoebe

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

## On Koios

Download the Miniforge3 installer and install it into your home directory, without changing
`~/.bashrc`:

```
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b -p $HOME/miniforge3
```

Activate it in each shell and at the start of batch job scripts:

```
source $HOME/miniforge3/etc/profile.d/conda.sh
```

The rest of this page works the same, with this line in place of the two Phoebe lines.

## Create and use an environment

```
conda create --name myenv python=3.12
conda activate myenv
```

With the Phoebe module, the defaults work without a `~/.condarc`:

* Environments go to `~/.conda/envs`, so they are available on all compute nodes.
* Downloaded packages are cached in `~/.conda/pkgs`.
* The module's own `base` environment is on CVMFS and read only: create your own environment
  instead of installing packages into `base`.

On Koios, environments and the package cache are in `~/miniforge3/envs` and `~/miniforge3/pkgs`.

A small Python environment takes about 250 MB, and the package cache grows with every
environment you create. Home directories have no quota, but the storage is shared (see
[storage](../systems/storage.md)), so remove environments you no longer use and clean the cache
from time to time:

```
conda env remove --name myenv
conda clean --all
```

To share one environment with your project group, create it in the project directory with
`--prefix` and activate it by path:

```
conda create --prefix /mnt/proj/pNNN_name/envs/myenv python=3.12
conda activate /mnt/proj/pNNN_name/envs/myenv
```

## In a batch job

On Phoebe:

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

On Koios, replace the `module load` and first `source` line with
`source $HOME/miniforge3/etc/profile.d/conda.sh`.

## Guides that use conda

* [CuPy on GPUs](cupy.md)
* [Pyoperon](pyoperon.md)
* [CosmoSIS with Python 2.7](cosmosis-py27.md)
