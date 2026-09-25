---
title: "Phoebe: project001 exclusive per user, GPU partitions no longer preemptable"
date: 2026-07-28
slug: project001-exclusive-user
---

# Phoebe: project001 exclusive per user, GPU partitions no longer preemptable

Changes to the Phoebe Slurm configuration between mid-May and 28 July 2026.

<!-- more -->

## GPU partitions no longer preemptable

`gpu` and `gpu_int` got `PreemptMode=OFF`. Jobs there are never suspended, while jobs in
`gpu1` and `gpu2` can still be suspended by `gpu_int` jobs.

## Controller rate limiting

`SlurmctldParameters` gained `rl_bucket_size=300,rl_refill_rate=100`, raising the limits of
the controller's per-user RPC rate limiting (`rl_enable`).

## project001: exclusive per user

The `project001` partition changed from `OverSubscribe=EXCLUSIVE` (a job gets whole nodes) to
`ExclusiveUser=YES` (nodes are shared only between jobs of the same user).

!!! warning "TODO"
    Add the dates of the first two changes (they happened between 14 May and 28 July) and the
    reasons for all three.
