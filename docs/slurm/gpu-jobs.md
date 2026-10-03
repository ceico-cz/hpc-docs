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
| `gpu` | `gpu[1-2]` | 18 days 8 h | batch GPU jobs; never paused |
| `gpu1`, `gpu2` | one node | 14 days 4 h | pin a batch job to one node; can be paused while an interactive GPU job needs the node |
| `gpu_int` | `gpu[1-2]` | 20 days 10 h | [interactive](interactive.md) GPU work |

For most batch jobs, use `gpu`. See [preemption](index.md#preemption-when-a-job-can-be-paused-or-stopped)
for what "paused" means.

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
#SBATCH --partition=gpu
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
srun --partition=gpu_int --gres=gpu:a100:1 --cpus-per-task=8 --time=04:00:00 --pty bash
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

CUDA is available as modules on every node, from `CUDA/11.4.1` to `CUDA/13.3.0`. The GPU
nodes' driver runs all of them.

GPU frameworks such as PyTorch, TensorFlow and CuPy are not provided as modules. Install them
yourself with [conda](../software/conda.md) or [uv](../software/python-uv.md); see
[CuPy on GPUs](../software/cupy.md) for an example. See also
[software modules](../software/modules.md).
