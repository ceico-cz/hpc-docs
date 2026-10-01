---
title: "Koios"
wikijs_updated: 2023-11-10
description: "Koios, the previous-generation CEICO cluster"
---

# Koios

Koios is the previous-generation CEICO cluster. It has 27 compute nodes, each with two 16-core
Intel Xeon Skylake CPUs ([Xeon Gold 6130](infrastructure.md#intel-xeon-gold-6130)) and 384 GB of RAM.
All nodes run Rocky Linux 9.8.

!!! info "GPU node temporarily unavailable"
    The GPU node with four [NVIDIA Tesla P100](infrastructure.md#nvidia-tesla-p100) cards is currently
    dedicated to a project and is not available through Slurm. It will return to general use
    later. Until then, use the A100 nodes on [Phoebe](../phoebe/index.md) for GPU work.

## Accessing Koios

Log in through the front-end node `koios1.fzu.cz` (see [SSH](../../getting-started/ssh.md)).
Koios shares accounts and SSH keys with Phoebe, so the same username and key work on both. Its
home directories are separate from Phoebe's.

## Slurm partitions

Jobs on Koios are managed by [Slurm](../../slurm/index.md). Jobs go to the `cpu` partition unless
you ask for another one with `--partition`.

| Partition | Nodes | Per node | Time limit | Use |
| --- | --- | --- | --- | --- |
| `cpu` (default) | `n[1-9,11-27]` | 32 cores (64 threads), 384 GB | 9 days 1 h | batch jobs |
| `cpu_int` | `n[11-12]` | 32 cores (64 threads), 384 GB | 9 days 1 h | interactive work |
| `preempt` | `n8` | 32 cores (64 threads), 384 GB | 9 days 1 h | jobs that may be preempted |
| `small_int` | `s1` (virtual machine) | 8 cores, 23 GB | 7 days 7 h | jobs that need only a small node |
| `rocky10` | `n12` | 32 cores (64 threads), 384 GB | 9 days 1 h | testing Rocky Linux 10 |

!!! warning "TODO"
    Confirm that `rocky10` is meant for users.

Limits change from time to time; `sinfo` on the login node shows the current values.

## Hardware

| Node type | Amount | Hostnames | Processors | GPUs | Cores (logical CPUs) | Main memory | NVMe |
| --- | --- | --- | --- | --- | --- | --- | --- |
| compute | 27 | `n[1-27]` | 2× [Xeon Gold 6130](infrastructure.md#intel-xeon-gold-6130) | - | 32 (64) | 384 GB | 1× 2 TB |
| GPU | 1 | `gpu2` | 2× [Xeon Gold 6130](infrastructure.md#intel-xeon-gold-6130) | 4× [Tesla P100](infrastructure.md#nvidia-tesla-p100) SXM2 16 GB | 32 (virtual) | 293 GB | - |

The GPU node is a virtual machine. It uses 32 of the 64 logical CPUs of its physical server,
and the four GPUs are passed through to it directly. It is currently dedicated to a project
(see the note at the top of this page).

The nodes are connected by 100 Gb/s InfiniBand EDR (Mellanox MT4115 ConnectX-4 cards), a
low-latency network for communication between nodes. More detail: [Koios infrastructure](infrastructure.md).

## Storage and software

Koios has its own home directories, software tree (`/cvmfs/c9.phoebe.lan`) and shared scratch
(`/mnt/shared-scratch`); the project space `/mnt/proj` is the same as on Phoebe. Each job gets a
private `/tmp` on the node's NVMe disk. See [storage and software](../storage.md).
