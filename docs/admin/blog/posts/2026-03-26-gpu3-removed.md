---
title: "Phoebe: P100 node gpu3 removed, login and service partitions added"
date: 2026-03-26
slug: gpu3-removed
---

# Phoebe: P100 node gpu3 removed, login and service partitions added

Two changes to the Phoebe Slurm configuration on 26 March 2026.

<!-- more -->

## gpu3 and the gpu_koios partition removed

`gpu3` was a small node (8 cores, 125 GB of RAM) with one NVIDIA Tesla P100, available through
the `gpu_koios` partition with a 5-day time limit. Both were removed from `slurm.conf`, and
`gpu3` was dropped from `SuspendExcNodes`. Its `gres.conf` line stayed until after May 2026.

!!! warning "TODO"
    Say why gpu3 was removed and where the card went.

## Hidden login and service partitions

Two hidden partitions were added: `login` on `login1` and `service` on `ondemand[1-2]`, both
with 3000 MB per CPU and a limit of 7 days 7 h. They don't appear in `sinfo` for users.

!!! warning "TODO"
    Say what runs in these partitions (for example Open OnDemand services or login-node jobs).
