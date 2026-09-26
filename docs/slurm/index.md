---
title: "Running jobs with Slurm"
wikijs_updated: 2023-11-16
description: "How jobs run on Phoebe and Koios: Slurm commands, defaults, limits and preemption"
---

# Running jobs with Slurm

Phoebe and Koios both use the [Slurm](https://slurm.schedmd.com) workload manager. You log in
to a front-end node and ask Slurm for resources; Slurm starts your work on compute nodes when
the resources are free. Each cluster has its own Slurm, so a job submitted on Phoebe runs
only on Phoebe.

* [Batch jobs](batch-jobs.md): write a job script and submit it with `sbatch`
* [GPU jobs](gpu-jobs.md): request A100 GPUs on Phoebe
* [Interactive sessions](interactive.md): get a shell on a compute node with `srun`
* [Job history and troubleshooting](troubleshooting.md): find out why a job failed or is still waiting

The partitions (groups of nodes with their own time limits) are listed on the system pages:
[Phoebe partitions](../systems/phoebe/index.md#slurm-partitions) and
[Koios partitions](../systems/koios/index.md#slurm-partitions). On Phoebe, `sinfo` also shows the
partitions `debug` and `project001`; they are reserved, so don't submit jobs to them.

## Common commands

| Command | What it does |
| --- | --- |
| `sbatch job.sh` | submit a batch job script |
| `srun --pty bash` | start an interactive shell on a compute node (add resource options) |
| `squeue --me` | list your queued and running jobs |
| `scancel <jobid>` | cancel a job |
| `sacct` | show your recent jobs, including finished ones |
| `scontrol show job <jobid>` | show every detail of one job |
| `sinfo` | show partitions, their time limits and node states |
| `sshare` | show your fair-share usage |

## Defaults worth knowing

### Always set a time limit

No partition has a default time limit. A job without `--time` gets the partition's maximum
(18 days on Phoebe's `cpu` partition), and Slurm then has to find a free slot that long, so
the job usually waits longer. Ask for roughly twice what you expect the job to need.

### Memory per CPU

If you do not ask for memory with `--mem` or `--mem-per-cpu`, a job gets a fixed amount per
allocated CPU:

| Cluster | Partitions | Default memory per CPU |
| --- | --- | --- |
| Phoebe | `cpu`, `cpu_int`, `preempt` | 2 GB |
| Phoebe | `gpu`, `gpu1`, `gpu2`, `gpu_int` | 16 GB |
| Phoebe | `small_int` | 3.5 GB |
| Koios | all partitions | 3 GB |

A job that uses more memory than it has is killed with the state `OUT_OF_MEMORY`.

On the CPU nodes of both clusters, a "CPU" in Slurm is one hardware thread; every core has
two. `--cpus-per-task=64` on a Phoebe CPU node therefore gets 32 physical cores. Slurm hands out
whole cores, so an odd number of CPUs is rounded up: `--cpus-per-task=1` gets 2 CPUs, and with
them twice the default memory per CPU.

### Per-user limits

| Cluster | Limit |
| --- | --- |
| Phoebe | at most 16 A100 GPUs and 3000 running jobs per user |
| Koios | none below the size of the cluster |

Some users and projects have their own limits. If your job waits with a reason starting with
`QOS` or `Assoc`, you have reached one; see
[why is my job pending?](troubleshooting.md#why-is-my-job-pending).

### Priority and fair share

A pending job's priority is the sum of three parts:

* **QOS**: a fixed amount set by your QOS. Most users have the `normal` QOS, which gives every
  job the same amount. A few special QOS with their own CPU or GPU limits add nothing, so their
  jobs usually queue behind jobs with `normal`.
* **Fair share**: the less you have used the cluster recently, the more priority your jobs get.
  The usage that counts is reset every week.
* **Age**: jobs gain a little priority while they wait, for up to 7 days.

`sprio -w` shows how much each part can add at most:

```
$ sprio -w
          JOBID PARTITION   PRIORITY       SITE        AGE  FAIRSHARE        QOS
        Weights                               1       1000     100000     100000
```

In practice the QOS part is the largest. `sprio -u $USER` shows the parts for your pending
jobs, and `sshare` your usage.

## Preemption: when a job can be paused or stopped

Some partitions rank higher than others. When a job in a higher-ranked partition needs nodes,
Slurm can pause or stop jobs from lower-ranked partitions on the same nodes:

* **Suspended**: on Phoebe, jobs in the interactive partitions `cpu_int` and `gpu_int` rank
  above the batch partitions. A job in `cpu`, `gpu1` or `gpu2` can be paused while an
  interactive job needs its node, and continues afterwards. Jobs in `gpu` and `gpu_int` are
  never paused.
* **Requeued**: jobs in the `preempt` partition (on Phoebe and Koios) are stopped and put back
  in the queue when a job from one of the regular partitions needs the node. Use it only for
  jobs that can restart from the beginning or from a checkpoint. In return it lets you use
  idle nodes that would otherwise sit unused.

A requeued job shows as `PREEMPTED` in `sacct`.
