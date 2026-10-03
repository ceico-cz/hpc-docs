---
title: "GPU profiling with Nsight"
description: "Profile CUDA kernels on Phoebe's A100 GPUs with Nsight Compute and Nsight Systems"
tags:
  - "slurm"
  - "gpu"
  - "profiling"
---

# GPU profiling with Nsight

NVIDIA's profilers are installed on both GPU nodes, `gpu1` and `gpu2`:

- **Nsight Systems** (`nsys`) shows a timeline of your program: CUDA API calls, kernels,
  memory copies, MPI and OpenMP, and your own NVTX ranges. Start here to see where the time
  goes.
- **Nsight Compute** (`ncu`) measures single kernels in detail: achieved occupancy, memory
  throughput, and why a kernel is slow.

`nsys` is on the default `PATH`. `ncu`, `compute-sanitizer` and `cuda-gdb` are in
`/usr/local/cuda/bin`; add it to your `PATH` first:

```shell
export PATH=/usr/local/cuda/bin:$PATH
```

## When you need `--constraint=nsight`

The cluster monitors how jobs use their GPUs with NVIDIA DCGM. DCGM reads the GPUs' hardware
performance counters all the time, and only one tool can use these counters at once. Tools
that read them need the job option `--constraint=nsight`:

| Tool | Needs `--constraint=nsight` |
| --- | --- |
| `ncu` (Nsight Compute) | yes |
| `nsys --gpu-metrics-devices=...` | yes |
| `nsys` without GPU metrics (timeline of CUDA calls, kernels, NVTX, MPI) | no |
| `compute-sanitizer`, `cuda-gdb` | no |

With `--constraint=nsight`, DCGM stops reading the counters on the node for as long as your
job runs. Your job, and other jobs on the same node, then have no GPU efficiency data for
that time. Use the option only for jobs that profile.

## Batch job example

```shell
#!/bin/bash
#SBATCH --job-name=ncu-profile
#SBATCH --partition=rocky10
#SBATCH --constraint=nsight
#SBATCH --time=01:00:00
#SBATCH --gpus=1
#SBATCH --cpus-per-task=8

export PATH=/usr/local/cuda/bin:$PATH

# Profile the first 5 launches of the kernel "my_kernel"
ncu --kernel-name my_kernel --launch-count 5 \
    --set detailed -o my_kernel_report ./my_program
```

`ncu` writes `my_kernel_report.ncu-rep` to the current directory. Profiling with all
sections (`--set full`) can make a program hundreds of times slower, so limit it to the
kernels and launches you are interested in (`--kernel-name`, `--launch-skip`,
`--launch-count`).

For a timeline with Nsight Systems:

```shell
nsys profile --trace=cuda,nvtx,osrt -o my_timeline ./my_program
```

That needs no constraint. Add `--gpu-metrics-devices=all` and `--constraint=nsight` to also
sample GPU metrics such as SM activity and memory bandwidth along the timeline.

## Interactive example

```shell
srun --partition=rocky10 --constraint=nsight --gpus=1 --cpus-per-task=8 --time=02:00:00 --pty bash
export PATH=/usr/local/cuda/bin:$PATH
ncu --kernel-name my_kernel --launch-count 1 ./my_program
```

## Look at the results

Copy the report files (`.ncu-rep`, `.nsys-rep`) to your computer and open them in the
Nsight Compute or Nsight Systems application, which NVIDIA offers as a free download for
Linux, Windows and macOS. For a quick look in the terminal:

```shell
ncu --import my_kernel_report.ncu-rep --page details
nsys stats my_timeline.nsys-rep
```

## Troubleshooting

`Profiling failed because a driver resource was unavailable. Ensure that no other tool (like DCGM) is concurrently collecting profiling data.`
:   The job was submitted without `--constraint=nsight`. Submit it again with the option.

`ERR_NVGPUCTRPERM - The user does not have permission to access NVIDIA GPU Performance Counters`
:   GPU performance counters are not yet open to all users on that node. Please contact the
    administrators.

`Invalid feature specification`
:   `--constraint=nsight` was used in a partition without GPU nodes.
