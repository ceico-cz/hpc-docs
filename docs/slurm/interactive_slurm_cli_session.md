---
title: "Interactive Slurm CLI session"
wikijs_updated: 2025-09-05
description: "HOW to run your commands at compute node"
tags:
  - "cli, ssh, slurm"
---

# Interactive Slurm CLI session

## Procedure

### Log in to the front-end node

```
user@jose-t14s:~$ ssh phoebe.fzu.cz -l jose
Welcome at CEICO (www.ceico.cz) computing facilities :)
Last login: Tue Jan 30 16:58:54 2024 from phoebe-gw.fzu.cz
[user@login1 ~]$
```

### Start a screen session to hold your Slurm job

Here we create slurm session with name "session007":

```
[user@login1 ~]$ screen -S session007
```

### Specify resources you need

In this example, we'll request resources in gpu2 partition.

### Request resources from Slurm

#### Example 1: 128 CPUs and 2 GPUs on any GPU node

```
srun --part=gpu_int --job-name "interactiveshell" --cpus-per-task=128 --mem=128G --time=24:00:00 --gres=gpu:a100:2 --pty /bin/bash
```



#### Example 2: 16 CPUs on a node in the gpu2 partition

```
[user@login1 ~]$ srun --part=gpu2 --job-name "interactivesheell" --cpus-per-task=16 --mem=128G --time=24:00:00 --pty /bin/bash
srun: job 1962744 queued and waiting for resources
srun: job 1962744 has been allocated resources
[user@gpu2 ~]$
```

##### Notes

Upon initiation, the shell opens, granting access for interactive tasks on the designated node — such as launching IPython sessions. Note that the job is set to conclude within a designated timeframe, as illustrated in this instance, within 24 hours.

Note, that the prompt changed from `user@login1` to `user@gpu2`, indicating that we were assigned resources at compute node `gpu2`.
