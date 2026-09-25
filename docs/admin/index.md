---
title: "Administration"
wikijs_updated: 2024-04-08
description: "Notes for the administrators of the CEICO clusters and lab machines"
---

# Administration

Notes from running the CEICO clusters and lab machines. Most commands on these pages need
root or Slurm administrator rights; as a user, see [Running jobs](../slurm/index.md) and
[Software](../software/modules.md) instead.

## Slurm

* [Accounting and limits](slurm-accounting.md) - QOS, per-user CPU and GPU limits, accounting users
* [Operational snippets](slurm-snippets.md) - resuming jobs, maintenance reservations

## Nodes

* [CUDA driver and toolkit](cuda.md) - installing a driver and CUDA version that match the NVIDIA containers
* [Add an LVM volume](lvm-volume.md) - adding a logical volume to a compute node whose disk is already full (work in progress)

## Lab equipment

* [Advantech USB-5855 on Ubuntu](advantech-usb-5855.md) - getting the USB digital I/O module working under Ubuntu 23.10
