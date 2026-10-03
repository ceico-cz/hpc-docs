---
title: "GPU jobs"
description: "Request NVIDIA A100 GPUs on Phoebe in batch jobs and interactive sessions"
tags:
  - "slurm"
  - "gpu"
---

# GPU jobs

Phoebe has two GPU nodes, `gpu1` and `gpu2`, each with 8 NVIDIA A100 80 GB cards, 64 CPU
cores and 2 TB of RAM. Koios has no GPUs available through Slurm.

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

The `CUDA/...` modules of the other nodes are not available on the GPU nodes yet.

GPU frameworks such as PyTorch, TensorFlow and CuPy are not provided as modules. Install them
yourself with [conda](../software/conda.md) or [uv](../software/python-uv.md); see
[CuPy on GPUs](../software/cupy.md) for an example. See also
[software modules](../software/modules.md).
