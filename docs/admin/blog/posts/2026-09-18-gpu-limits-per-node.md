---
title: "Phoebe: limiting GPUs per user per node"
date: 2026-09-18
slug: gpu-limits-per-node
---

# Phoebe: limiting GPUs per user per node

How to give a user a GPU limit per node (for example 3 GPUs on `gpu1` and 3 on `gpu2`) instead
of one limit across the whole cluster, and why the setup tried on 18 September 2026 was removed
again the same day.

<!-- more -->

## How Slurm counts GPUs

| Limit | What it counts |
|---|---|
| QOS `MaxTRESPU=gres/gpu=N` | GPUs of all running jobs of a user with that QOS, in every partition that uses it |
| QOS `MaxTRESPerJob` | each job on its own |
| QOS `MaxTRESPerNode` | each job on each of its nodes, not the sum of a user's jobs on a node |
| Association `GrpTRES=gres/gpu=N` with `Partition=` | GPUs of a user's running jobs in that one partition |

A QOS or an association can be tied to a partition, but not to a physical node. A QOS with
`MaxTRESPU=gres/gpu=3` used on the shared `gpu` and `gpu_int` partitions (both contain `gpu1`
and `gpu2`) therefore means 3 GPUs per user in total. A job waits with `QOSMaxGRESPerUser` once
the user has 3 GPUs running on `gpu2`, even if `gpu1` has free GPUs.

## Setting up per-node limits

Phoebe also has the single-node partitions `gpu1` and `gpu2`. A separate counter per node needs
one QOS per node, each used only in that node's partition:

```bash
sacctmgr add qos gpu1_max3 MaxTRESPU=gres/gpu=3 MaxTRESPerJob=gres/gpu=3 Flags=DenyOnLimit
sacctmgr add qos gpu2_max3 MaxTRESPU=gres/gpu=3 MaxTRESPerJob=gres/gpu=3 Flags=DenyOnLimit

sacctmgr add user USER cluster=phoebe account=ACCOUNT partition=gpu1 \
    qos=gpu1_max3 defaultqos=gpu1_max3
sacctmgr add user USER cluster=phoebe account=ACCOUNT partition=gpu2 \
    qos=gpu2_max3 defaultqos=gpu2_max3
```

Copy the CPU and memory limits of the user's current QOS into the new ones. Without
`DenyOnLimit`, a job that asks for too many GPUs is accepted and stays pending forever instead
of being rejected at submission.

The user then submits with `--partition=gpu1` or `--partition=gpu2`. Their access to `gpu` and
`gpu_int` has to be closed, because jobs there are not counted against the per-node QOS. That
can be done with `DenyQos=` on those partitions in `slurm.conf`, or by removing the user's
`gpu` and `gpu_int` associations.

Check the result with `sbatch --test-only`: 3 GPUs on `gpu1` should be accepted and 4 rejected,
and a job on `gpu` or `gpu_int` should be rejected.

## Things to watch

* **Jobs that are already running stay on their old QOS.** Slurm changes the QOS only of
  pending jobs (`scontrol update JobId=... QOS=...`); for a running job it fails with "Job is no
  longer pending execution". Until those jobs end, their GPUs are not counted by the new QOS,
  so the new limit can be exceeded. Either wait for them to finish or keep the new QOS blocked
  on that node (for example with `DenyQos=`) until they do.
* **Moving a pending job** to `gpu1` or `gpu2` can mean a shorter time limit, because those
  partitions have a lower `MaxTime` than `gpu` and `gpu_int`.
* **A failed `scontrol update` can apply part of the change.** Check the job with
  `scontrol show job` afterwards.
* **There is no cumulative per-node limit on the shared partitions.** As long as the user
  submits to `gpu` or `gpu_int`, no QOS or association setting limits their total GPUs on one
  node.

## What was done on 18 September

The two QOS, the `gpu1` and `gpu2` associations and `DenyQos=` entries on the `gpu`, `gpu1`,
`gpu2` and `gpu_int` partitions were set up and tested, but the new QOS were not switched on:
running jobs could not be moved to them. The setup was then dropped, because users should keep
submitting to `gpu` and `gpu_int` rather than pick a node themselves. The QOS, the associations
and the `DenyQos=` entries were removed, and the 3-GPU limit across both nodes (`gpu_max2`)
stayed as it was. See [accounts, QOS and limits](../../slurm-accounting.md).
