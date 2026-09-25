---
title: "Slurm admin snippets"
wikijs_updated: 2024-06-11
description: "Snippets from day-to-day Slurm administration"
tags:
  - "admin"
  - "slurm"
---

# Slurm admin snippets

## Resume suspended jobs on a node

On Phoebe, jobs in `cpu`, `gpu1` and `gpu2` can be suspended by jobs in the higher-ranked
interactive partitions (`PreemptMode=GANG,SUSPEND`). They normally resume on their own. To
resume every suspended job on a node by hand, here `n14`:

```
for job in $(squeue --noheader --states=SUSPENDED -w n14 -o %i); do scontrol resume job=$job; done
```

Add `--user=<name>` to `squeue` to resume only one user's jobs.

## Drain and resume a node

Stop new jobs from starting on a node, while running jobs finish:

```
scontrol update nodename=n14 state=DRAIN reason="disk replacement"
```

Put it back into service:

```
scontrol update nodename=n14 state=RESUME
```

`sinfo -R` lists drained and down nodes with their reasons.

## Create a maintenance reservation

A `MAINT` reservation keeps jobs from running into a maintenance window. Jobs whose time limit
would overlap it wait with the reason `ReqNodeNotAvail, Reserved for maintenance`.
`Nodes=ALL` covers every node, so the command doesn't go stale when nodes change:

```
scontrol create reservation starttime=2026-10-14T18:00:00 duration=3-00:00:00 flags=MAINT,IGNORE_JOBS nodes=ALL user=root
```

Run it on each cluster's controller (Phoebe and Koios have separate Slurm instances).

List and delete reservations:

```
scontrol show reservation
scontrol delete reservation=root_1
```

## Reload the configuration

After editing `slurm.conf` or `gres.conf` on the controller:

```
scontrol reconfigure
```

Phoebe runs in configless mode, so nodes get their configuration from the controller and a
change takes effect only after `scontrol reconfigure`. It re-reads **all** configuration files,
so check that nothing else changed since the last reload. Changes to node definitions may need
a restart of `slurmctld` and the affected `slurmd`s instead.
