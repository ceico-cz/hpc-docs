---
title: "Koios"
wikijs_updated: 2023-11-10
description: "Koios, the previous-generation CEICO cluster"
---

# Koios

Koios is the previous-generation CEICO cluster. It has 27 compute nodes, each with two 16-core
Intel Xeon Skylake CPUs ([Xeon Gold 6130](hardware.md#intel-xeon-gold-6130)) and 384 GB of RAM.
All nodes run Rocky Linux 9.

!!! warning "TODO"
    Check the operating system: the Slurm partition `rocky10` on `n12` suggests a move to
    Rocky Linux 10 is under way.

!!! info "GPU node temporarily unavailable"
    The GPU node with four [NVIDIA Tesla P100](hardware.md#nvidia-tesla-p100) cards is currently
    dedicated to a project and is not available through Slurm. It will return to general use
    later. Until then, use the A100 nodes on [Phoebe](../phoebe/index.md) for GPU work.

## Accessing Koios

Log in through the front-end node `koios1.fzu.cz` (see [SSH](../../getting-started/ssh.md)).
Koios shares accounts, SSH keys and home directories with Phoebe, so the same username and key
work on both.

## Slurm partitions

Jobs on Koios are managed by [Slurm](../../slurm/index.md). Jobs go to the `cpu` partition unless
you ask for another one with `--partition`.

| Partition | Nodes | Per node | Time limit | Use |
| --- | --- | --- | --- | --- |
| `cpu` (default) | `n[1-9,11-27]` | 32 cores (64 threads), 384 GB | 9 days 1 h | batch jobs |
| `cpu_int` | `n[11-12]` | 32 cores (64 threads), 384 GB | 9 days 1 h | interactive work |
| `preempt` | `n8` | 32 cores (64 threads), 384 GB | 9 days 1 h | jobs that may be preempted |
| `small_int` | `s1` | 8 cores, 24 GB | 7 days 7 h | light interactive work |
| `rocky10` | `n12` | 32 cores (64 threads), 384 GB | 9 days 1 h | testing Rocky Linux 10 |

!!! warning "TODO"
    Confirm that `small_int` and `rocky10` are meant for users. `s1` is currently reported as
    invalid by Slurm.

Limits change from time to time; `sinfo` on the login node shows the current values.

## Hardware

| Node type | Amount | Hostnames | Processors | GPUs | Cores (logical CPUs) | Main memory | NVMe |
| --- | --- | --- | --- | --- | --- | --- | --- |
| compute | 27 | `n[1-27]` | 2× [Xeon Gold 6130](hardware.md#intel-xeon-gold-6130) | - | 32 (64) | 384 GB | 1× 2 TB |
| GPU | 1 | TODO | TODO | 4× [Tesla P100](hardware.md#nvidia-tesla-p100) | TODO | TODO | TODO |

The nodes are connected by 100 Gb/s InfiniBand EDR (Mellanox MT4115 ConnectX-4 cards), a
low-latency network for communication between nodes. More detail: [Koios hardware](hardware.md).

## Storage and software

Koios and Phoebe share home directories and the software tree; see
[storage and software](../storage.md).
