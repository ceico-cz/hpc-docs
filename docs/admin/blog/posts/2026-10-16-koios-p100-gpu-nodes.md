---
title: "Koios: two Tesla P100 GPU nodes in the gpu partition"
date: 2026-10-16
slug: koios-p100-gpu-nodes
---

# Koios: two Tesla P100 GPU nodes in the gpu partition

Since 16 October 2026 Koios has two GPU nodes again, `gpu3` and `gpu4`, each with two NVIDIA
Tesla P100 16 GB cards, in the new Slurm partition `gpu`. They replace the former GPU virtual
machine that held all four cards and was dedicated to a project.

<!-- more -->

## How to use them

Submit from `koios1.fzu.cz`, for example:

```shell
srun --partition=gpu --gres=gpu:p100:1 --cpus-per-task=16 --time=01:00:00 --pty bash
```

[GPU jobs](../../../compute/gpu-jobs.md#koios-tesla-p100) has batch and interactive examples and
the software on the nodes. In short:

* The P100 (Pascal, compute capability 6.0) is not supported by CUDA 13. The nodes have CUDA 12.9
  from the NVIDIA HPC SDK; build with `nvcc -arch=sm_60`.
* The nodes run Rocky Linux 10, and the Koios software tree `/cvmfs/c9.phoebe.lan` is not
  available there. Programs built on the Koios compute nodes may need to be rebuilt.
* Home directories, `/mnt/shared-scratch` and `/mnt/proj` are the same as on the rest of Koios.

## How it is set up

The four P100 cards sit in one server. Each node is a virtual machine on it with one of the
server's two CPUs (32 logical CPUs), the memory attached to that CPU (125 GB) and two GPUs
passed through directly; the two GPUs of a node are connected by one NVLink.

On `slurmserver2.koios`, `slurm.conf` got the two node lines with `Gres=gpu:p100:2`, the
partition `gpu` (`Nodes=gpu[3-4]`, open to all, `MaxTime=9-01:02:03`), the nodes in
`SuspendExcNodes`, and `AccountingStorageTRES=gres/gpu`, so `sacct` now records GPU use on Koios.
The GPU type comes from NVML autodetection (`gres.conf` `AutoDetect=nvml`). The nodes run
Slurm 25.11, the controller's release series.
