---
title: "GPU jobs"
description: "Request NVIDIA A100 GPUs on Phoebe and Tesla P100 GPUs on Koios in batch jobs and interactive sessions"
tags:
  - "slurm"
  - "gpu"
---

# GPU jobs

Phoebe has two GPU nodes, `gpu1` and `gpu2`, each with 8 NVIDIA A100 80 GB cards, 64 CPU
cores and 2 TB of RAM. Koios has two smaller GPU nodes, `gpu3` and `gpu4`, each with 2 NVIDIA
Tesla P100 16 GB cards; see [Koios: Tesla P100](#koios-tesla-p100) at the end of this page. The
sections before it are about Phoebe.

## Choose a partition

| Partition | Nodes | Time limit | Use |
| --- | --- | --- | --- |
| `rocky10` | `gpu[1-2]` | 14 days 4 h | batch and [interactive](interactive.md) GPU work; never paused |

The GPU nodes run Rocky Linux 10. The former GPU partitions `gpu`, `gpu1`, `gpu2` and
`gpu_int` no longer have nodes; jobs sent there do not start. To use one node only, add
`--nodelist=gpu1` or `--nodelist=gpu2`. Programs built on the Rocky 8 nodes may need to be
rebuilt for the GPU nodes.

## Request GPUs

Ask for GPUs with `--gres=gpu:a100:N`, where `N` is the number of cards on one node (1 to 8).
Slurm makes only the allocated cards visible to your job.

Each GPU node has 8 cores per GPU, so ask for about `--cpus-per-task=8` for every GPU you
request. That leaves room for other users' jobs on the same node. Without `--mem`, a job gets
16 GB of RAM per CPU.

You can use at most 16 GPUs at a time, across all your jobs.

## Batch job example

```shell
#!/bin/bash
#SBATCH --job-name=gpu-test
#SBATCH --partition=rocky10
#SBATCH --time=02:00:00
#SBATCH --gres=gpu:a100:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8

# shows only the GPU allocated to this job
nvidia-smi

python my_gpu_script.py
```

Submit it with `sbatch` as described in [batch jobs](batch-jobs.md).

## Interactive example

```shell
srun --partition=rocky10 --gres=gpu:a100:1 --cpus-per-task=8 --time=04:00:00 --pty bash
```

See [interactive sessions](interactive.md) for how to keep the session alive with `screen`.

## Check how your job uses its GPUs

The [job portal](https://jobs.phoebe.fzu.cz) shows, on the page of each job that ran on
`gpu1` or `gpu2`, how busy its GPUs were: SM activity (the share of time the GPU had work),
memory bandwidth, FP64 and tensor core use, GPU memory, power and energy. If SM activity
stays near zero, the job holds GPUs it does not use; ask for fewer GPUs, or check whether
your program runs on the GPU at all.

To find out why a kernel is slow, see [GPU profiling with Nsight](gpu-profiling.md).

## Software

The GPU nodes have CUDA 13.4 installed in `/usr/local/cuda` (add `/usr/local/cuda/bin` to your
`PATH`), and the NVIDIA HPC SDK compilers with HPC-X MPI as modules:

```shell
module use /opt/nvidia/hpc_sdk/modulefiles
module load nvhpc-hpcx-cuda13
```

The `CUDA/...` modules of the Rocky Linux 8 nodes are not available on the GPU nodes. Instead,
the [EESSI software stack](../software/eessi.md) has `CUDA` and `cuDNN` modules (CUDA 12.1 to
13.3) and GPU builds of applications such as GROMACS and LAMMPS:

```shell
source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
module avail CUDA cuDNN
```

This unloads modules you loaded before; see [EESSI](../software/eessi.md#keep-the-modules-you-already-loaded)
to combine it with the HPC SDK modules.

GPU frameworks such as PyTorch, TensorFlow and CuPy are not provided as modules. Install them
yourself with [conda](../software/conda.md) or [uv](../software/python-uv.md); see
[CuPy on GPUs](../software/cupy.md) for an example. See also
[software modules](../software/modules.md).

## Koios: Tesla P100

Koios has two GPU nodes, `gpu3` and `gpu4`, each with 2 NVIDIA
[Tesla P100](../systems/koios/infrastructure.md#nvidia-tesla-p100) 16 GB cards, 32 CPU cores and
125 GB of RAM. Submit jobs from the Koios login node `koios1.fzu.cz`; Koios has its own home
directories (see [Koios](../systems/koios/index.md)).

| Partition | Nodes | Time limit | Use |
| --- | --- | --- | --- |
| `gpu` | `gpu[3-4]` | 9 days 1 h | batch and interactive GPU work |

Ask for GPUs with `--gres=gpu:p100:N`, where `N` is 1 or 2. Slurm makes only the allocated cards
visible to your job. Ask for about `--cpus-per-task=16` per GPU. Without `--mem`, a job gets
3000 MB of RAM per CPU.

```shell
#!/bin/bash
#SBATCH --job-name=p100-test
#SBATCH --partition=gpu
#SBATCH --time=02:00:00
#SBATCH --gres=gpu:p100:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16

nvidia-smi
```

Interactively:

```shell
srun --partition=gpu --gres=gpu:p100:1 --cpus-per-task=16 --time=04:00:00 --pty bash
```

!!! warning "The P100 is an older GPU"
    The P100 (Pascal, CUDA compute capability 6.0) is not supported by CUDA 13 or newer, so
    software built for Phoebe's A100 nodes or with a current CUDA may not run on it. The GPU
    nodes run Rocky Linux 10, unlike the Koios compute nodes (Rocky Linux 9.8), and the Koios
    software tree `/cvmfs/c9.phoebe.lan` is not available on them.

### Software on the P100 nodes

The nodes have **CUDA 12.9**, the last CUDA release that can build code for the P100. It comes
with the NVIDIA HPC SDK 26.5 in `/opt/nvidia/hpc_sdk/Linux_x86_64/26.5`. Put its `cuda/12.9`
directory first in your paths and build for `sm_60`:

```shell
SDK=/opt/nvidia/hpc_sdk/Linux_x86_64/26.5
export PATH=$SDK/cuda/12.9/bin:$PATH
export LD_LIBRARY_PATH=$SDK/cuda/12.9/lib64:$SDK/math_libs/12.9/lib64:$LD_LIBRARY_PATH

nvcc -arch=sm_60 -o app app.cu
# with cuBLAS, cuFFT, ...: add -I$SDK/math_libs/12.9/include -L$SDK/math_libs/12.9/lib64 -lcublas
```

`nvcc` warns that support for `sm_60` will be removed in a future release; add
`-Wno-deprecated-gpu-targets` to hide the warning. The HPC SDK also has CUDA 13.2, which cannot
build for the P100: do not use the `nvcc` in `$SDK/compilers/bin`, which uses CUDA 13.2. The
HPC SDK compilers there (`nvc`, `nvc++`, `nvfortran`) use CUDA 12.9 on these nodes, for example
`nvc++ -acc -gpu=cc60`.

For GPU frameworks such as PyTorch, TensorFlow or CuPy, install them yourself with
[conda](../software/conda.md) or [uv](../software/python-uv.md), and choose a version whose
CUDA build still supports compute capability 6.0 (`sm_60`): many recent releases do not.
