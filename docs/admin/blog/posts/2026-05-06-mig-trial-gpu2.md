---
title: "Phoebe: MIG trial on gpu2 and GPU node topology"
date: 2026-05-06
slug: mig-trial-gpu2
---

# Phoebe: MIG trial on gpu2 and GPU node topology

On 6 May 2026 two of gpu2's eight A100s were split into small MIG instances. The trial was
rolled back on 13–14 May. The CPU topology changes made at the same time stayed.

<!-- more -->

## CPU topology of the GPU nodes

Several attempts on 6 May changed how Slurm sees the CPUs of `gpu1` and `gpu2`:

1. `GetEnvTimeout=2` removed, and `Parameters=l3cache_as_socket` tried on `gpu2`.
2. Replaced by the cluster-wide `SlurmdParameters=numa_node_as_socket`.
3. `gpu1` and `gpu2` redefined from `Sockets=2 CoresPerSocket=32` to
   `Sockets=8 CoresPerSocket=8`: each NUMA node is now a socket.

With 8 "sockets" of 8 cores, each GPU can be bound to the cores closest to it.

## MIG on gpu2

`gpu2` was changed from `Gres=gpu:a100:8` to `Gres=gpu:a100:6,gpu:nvidia_a100_1g.10gb:14`:

* GPUs 0–3 and 6–7 stayed as full A100s.
* GPUs 4 and 5 were each split into seven `1g.10gb` MIG instances (14 in total).
* `gres.conf` listed every device by hand (`AutoDetect=off`), with the cores closest to each
  GPU.

On 13–14 May gpu2 went back to `Gres=gpu:a100:8`, with the original one-line `gres.conf`
entry. MIG is disabled on all eight cards today.

!!! warning "Typo introduced by the rollback"
    The restored `gres.conf` line reads `Nodename=gpu2Type=a100 ...` (no space before
    `Type`). It probably still works because `AutoDetect=nvml` finds the cards, but it should
    read `Nodename=gpu2 Type=a100 ...`.

!!! warning "TODO"
    Say why MIG was tried and why it was rolled back.
