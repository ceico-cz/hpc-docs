---
title: "Interactive sessions"
wikijs_updated: 2025-09-05
description: "Get a shell on a compute node to run commands interactively"
tags:
  - "cli"
  - "ssh"
  - "slurm"
---

# Interactive sessions

An interactive session gives you a shell on a compute node, for example to try out commands,
compile code or run IPython, before you write a [batch job](batch-jobs.md).

## Choose a partition

Use the interactive partitions. Jobs there start with higher priority than batch jobs.

| Cluster | Partition | Nodes | Time limit | Use |
| --- | --- | --- | --- | --- |
| Phoebe | `cpu_int` | `n[1-20]` | 20 days 10 h | CPU work |
| Phoebe | `gpu_int` | `gpu[1-2]` | 20 days 10 h | GPU work |
| Phoebe | `small_int` | `s[1-3]` | 7 days 7 h | light work (8 cores, 64 GB per node) |
| Koios | `cpu_int` | `n[11-12]` | 9 days 1 h | CPU work |

## Start a screen session

An interactive session ends when you disconnect. [Log in to the front-end node](../getting-started/ssh.md)
and start a `screen` session first, so the session survives a dropped connection. Here we
name it "session007":

```
[user@login1 ~]$ screen -S session007
```

Detach with ++ctrl+a++, then `d` (two separate key presses; see [screen sessions](../tips/screen.md)). To come back later, log in again and reattach:

```
[user@login1 ~]$ screen -r session007
```

## Request resources from Slurm

### Example 1: 16 CPUs on a CPU node

```
[user@login1 ~]$ srun --partition=cpu_int --job-name "interactive" --cpus-per-task=16 --mem=32G --time=08:00:00 --pty /bin/bash
srun: job 1962744 queued and waiting for resources
srun: job 1962744 has been allocated resources
[user@n11 ~]$
```

The prompt changed from `user@login1` to `user@n11`: you are now on compute node `n11`.

### Example 2: 2 GPUs and 16 CPUs on a GPU node

```
srun --partition=gpu_int --job-name "interactive" --gres=gpu:a100:2 --cpus-per-task=16 --mem=128G --time=24:00:00 --pty /bin/bash
```

See [GPU jobs](gpu-jobs.md) for how many CPUs to request per GPU.

## When you are done

The session ends when its time limit is reached or when you leave the shell with `exit`.
Exit as soon as you are done, so the resources are free for others.
