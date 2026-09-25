---
title: "Administration"
wikijs_updated: 2024-04-08
description: "Notes for the administrators of the CEICO clusters and lab machines"
---

# Administration

Notes from running the CEICO clusters and lab machines. Most commands on these pages need
root or Slurm administrator rights; as a user, see [Running jobs](../slurm/index.md) and
[Software](../software/index.md) instead.

## Reference

* [Accounts, QOS and limits](slurm-accounting.md) - the accounts and QOS on Phoebe, adding users and limits
* [Slurm admin snippets](slurm-snippets.md) - suspended jobs, draining nodes, maintenance reservations, reloading the configuration
* [CUDA driver and toolkit](cuda.md) - the driver and CUDA versions on the GPU nodes, and how to update them

## Admin blog

The [admin blog](blog/index.md) records changes to the clusters, newest first: for example the
MIG trial on gpu2 and changes to partition time limits. Guides tied to a point in time, such
as getting the Advantech USB-5855 I/O module working on Ubuntu 23.10, are posts there too.
