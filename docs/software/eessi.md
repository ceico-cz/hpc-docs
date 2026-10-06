---
title: "EESSI software stack"
description: "Use the EESSI software modules, including CUDA and cuDNN, on the Rocky Linux 10 GPU nodes"
tags:
  - "modules"
  - "eessi"
  - "cuda"
  - "gpu"
---

# EESSI software stack

[EESSI](https://www.eessi.io/docs/) (the European Environment for Scientific Software
Installations) is a shared stack of scientific software, built with
[EasyBuild](https://docs.easybuild.io/) and distributed over CVMFS under
`/cvmfs/software.eessi.io`. It provides compilers, MPI, libraries and applications as
[Lmod modules](modules.md), optimised for the CPU and GPU of the node you run on.

On Phoebe, EESSI is the module stack of the `rocky10` partition (`gpu1` and `gpu2`): the GPU
nodes have no Phoebe stacks (`2023a` to `2026a`, `system`) yet. EESSI is not loaded by
default; set it up in each job or interactive session as described below.

## Start EESSI

Run this in a job or an interactive session on the `rocky10` partition, with the version you
want:

```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
```

```
Modules purged before initialising EESSI
Module for EESSI/2025.06 loaded successfully
EESSI has selected x86_64/amd/zen3 as the compatible CPU target for EESSI/2025.06
EESSI has selected accel/nvidia/cc80 as the compatible accelerator target for EESSI/2025.06
```

EESSI picks the builds for the node's CPU (AMD Zen 3) and GPU (NVIDIA A100, compute
capability 8.0) by itself. After that, `module avail`, `module spider` and `module load` work
as described in [Software modules (Lmod)](modules.md).

This command unloads every module you had loaded before (`module purge`) and uses EESSI's own
Lmod. It works in any Bash script, including batch jobs.

### Keep the modules you already loaded

If you need modules from elsewhere next to EESSI, for example the NVIDIA HPC SDK, add EESSI to
the node's Lmod instead:

```bash
module use /cvmfs/software.eessi.io/init/modules
module load EESSI/2025.06
```

`module use` takes the directory, not the `EESSI/<version>.lua` file inside it, and
`module avail EESSI` lists the versions. Modules you loaded before stay loaded. Don't combine
compilers or MPI libraries from EESSI with those of other stacks in one program.

## Choose a version

| Version | Toolchains | GPU modules |
| --- | --- | --- |
| `2026.06` | `foss/2026.1` (GCC 15.2) | `CUDA/13.3.0`, `cuDNN/9.23.0.39-CUDA-13.3.0` |
| `2025.06` | `foss/2024a` to `foss/2025b` (GCC 13.3 to 14.3) | `CUDA/12.6.0`, `12.8.0`, `12.9.1`; `cuDNN/9.5.0.50-CUDA-12.6.0`, `9.10.1.4-CUDA-12.8.0`, `9.15.0.57-CUDA-12.9.1`; GPU builds of GROMACS, ESPResSo, Siesta, NCCL, ollama and others |
| `2023.06` | `foss/2022b` to `foss/2023b` (GCC 12.2 to 13.2) | `CUDA/12.1.1`, `12.4.0`; `cuDNN/8.9.2.26-CUDA-12.1.1`; GPU builds of GROMACS, LAMMPS, ESPResSo, LightGBM, NCCL and others |

For new work, take the newest version that has what you need. Each version is a separate
stack: load modules from one version only.

## GPU software

On the GPU nodes, EESSI also lists its CUDA builds. A quick test (`CUDA-Samples` is in
`2023.06` and `2025.06`):

```bash
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module load CUDA-Samples
deviceQuery
```

It ends with `Result = PASS`.

NVIDIA's licences do not allow EESSI to ship CUDA and cuDNN, so they are installed on the GPU
nodes, which makes the `CUDA` and `cuDNN` modules in the table above work.

### Compile against EESSI libraries

EESSI modules do not set `LD_LIBRARY_PATH`. If you compile your own code against an EESSI
library such as cuDNN, link it with an RPATH so that it finds the library at run time:

```bash
module load CUDA/12.9.1 cuDNN/9.15.0.57-CUDA-12.9.1
nvcc -o app app.cu -lcudnn \
    -Xlinker --disable-new-dtags -Xlinker -rpath=$EBROOTCUDNN/lib:$EBROOTCUDA/lib64
```

`--disable-new-dtags` matters for cuDNN, which loads cuBLAS itself at run time.

## Batch job example

```bash
#!/bin/bash
#SBATCH --job-name=eessi-test
#SBATCH --partition=rocky10
#SBATCH --time=00:10:00
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=4

source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module load CUDA-Samples
deviceQuery
```

See [GPU jobs](../slurm/gpu-jobs.md) for requesting GPUs.

## Known issues

* If you have saved module collections (`module save`), starting EESSI may print
  `Lmod Warning: The system MODULEPATH has changed: please rebuild your saved collection.`
  It is harmless. Collections saved with the Phoebe stacks don't work on the GPU nodes;
  save new ones with EESSI modules if you need them.
* EESSI is meant for the `rocky10` partition. Its CUDA and cuDNN modules work only on the
  GPU nodes.

## Further reading

* [EESSI documentation](https://www.eessi.io/docs/)
* [Software available in EESSI](https://www.eessi.io/docs/available_software/overview/)
* [GPU support in EESSI](https://www.eessi.io/docs/site_specific_config/gpu/)
