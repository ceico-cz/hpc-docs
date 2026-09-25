---
title: "Create a conda environment with CuPy"
wikijs_updated: 2023-10-27
description: "Cupy is CUDA-aware numpy and scipy implementation"
tags:
  - "conda"
  - "cuda"
  - "cupy"
  - "gpu"
  - "python"
---

# Create a conda environment with CuPy

!!! tip "Ready-made module"
    An older CuPy is available as the module `CuPy/12.0.0-foss-2022a`, but only on the compute
    and GPU nodes (the `2022a` stack is not mounted on the login node). Build your own conda
    environment if you need a newer CuPy or CUDA version. For getting conda itself, see
    [Conda on Phoebe](conda.md).

## Get an interactive shell on a GPU node

From Phoebe login node, request 16CPUs, some RAM and one NVIDIA A100:

`srun --part=gpu_int --job-name "Conda build at GPU" --gres=gpu:a100:1 --cpus-per-task=16 --mem=128G --time=24:00:00 --pty bash`


**example**

```
[user@login1 ~]$ srun --part=gpu_int --job-name "Conda build at GPU" --gres=gpu:a100:1 --cpus-per-task=16 --mem=128G --time=24:00:00 --pty bash
srun: job 1401058 queued and waiting for resources
srun: job 1401058 has been allocated resources
[user@gpu2 ~]$
```

(note that the last prompt changed, and we're now inside of interactive slurm session at gpu2 compute node)

## Create an empty conda environment

Note: to have CUDA detection properly working, this must be done on gpu node.

First, create new conda environment with recent python included:

`conda create --name cupy-231030 python=3.11`

example:

```
[jose@gpu2 ~]$ conda create --name cupy-231030 python=3.11
Collecting package metadata (current_repodata.json): done
...
Proceed ([y]/n)? y
...
[jose@gpu2 ~]$
```

## Activate the new environment and install CUDA into it

we install from NVIDIA conda channel because we need nvcc and other dependencies

`conda activate cupy-231030`
`conda install -c "nvidia/label/cuda-12.3.0" cuda-toolkit`

## Install CuPy for the given CUDA version

above we installed cuda-12-x so:

`python3.11 -m pip install cupy-cuda12x`
