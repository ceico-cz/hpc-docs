---
title: "Phoebe: per-user GPU QOS restriction removed"
date: 2026-09-18
slug: gpu-qos-removed
---

# Phoebe: per-user GPU QOS restriction removed

On 18 September 2026 the `DenyQos=` entries were removed from the `gpu`, `gpu1`, `gpu2` and
`gpu_int` partitions.

<!-- more -->

They blocked two QOS that had been created for one user, one per GPU node (judging by their
names, each allowed at most 3 GPUs). The user now has the `gpu_max2` QOS (3 GPUs, 16 CPUs per job) instead; see
[accounts, QOS and limits](../../slurm-accounting.md).

!!! warning "TODO"
    Say why the per-node QOS were replaced.
