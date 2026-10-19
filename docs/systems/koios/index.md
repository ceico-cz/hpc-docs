---
title: "Koios"
wikijs_updated: 2023-11-10
description: "Koios, the previous-generation CEICO cluster"
---

# Koios

Koios is the previous-generation CEICO cluster. It has 27 compute nodes, each with two 16-core
Intel Xeon Skylake CPUs ([Xeon Gold 6130](infrastructure.md#intel-xeon-gold-6130)) and 384 GB of RAM,
and two GPU nodes, `gpu3` and `gpu4`, each with two [NVIDIA Tesla P100](infrastructure.md#nvidia-tesla-p100)
cards. The compute nodes run Rocky Linux 9.8, the GPU nodes Rocky Linux 10.

## Accessing Koios

Log in through the front-end node `koios1.fzu.cz` (see [SSH](../../getting-started/ssh.md)).
Koios shares accounts and SSH keys with Phoebe, so the same username and key work on both. Its
home directories are separate from Phoebe's.

## Slurm partitions

Jobs on Koios are managed by [Slurm](../../compute/index.md). Jobs go to the `cpu` partition unless
you ask for another one with `--partition`.

| Partition | Nodes | Per node | Time limit | Use |
| --- | --- | --- | --- | --- |
| `cpu` (default) | `n[1-9,11-27]` | 32 cores (64 threads), 384 GB | 9 days 1 h | batch jobs |
| `cpu_int` | `n[11-12]` | 32 cores (64 threads), 384 GB | 9 days 1 h | interactive work |
| `preempt` | `n8` | 32 cores (64 threads), 384 GB | 9 days 1 h | jobs that may be preempted |
| `small_int` | `s1` (virtual machine) | 8 cores, 23 GB | 7 days 7 h | jobs that need only a small node |
| `gpu` | `gpu[3-4]` (virtual machines) | 2 Tesla P100, 32 cores, 125 GB | 9 days 1 h | [GPU jobs](../../compute/gpu-jobs.md#koios-tesla-p100) |

Limits change from time to time; `sinfo` on the login node shows the current values.

## Hardware

| Node type | Amount | Hostnames | Processors | GPUs | Cores (logical CPUs) | Main memory | NVMe |
| --- | --- | --- | --- | --- | --- | --- | --- |
| compute | 27 | `n[1-27]` | 2× [Xeon Gold 6130](infrastructure.md#intel-xeon-gold-6130) | - | 32 (64) | 384 GB | 1× 2 TB |
| GPU | 2 | `gpu[3-4]` | 1× [Xeon Gold 6130](infrastructure.md#intel-xeon-gold-6130) (virtual) | 2× [Tesla P100](infrastructure.md#nvidia-tesla-p100) SXM2 16 GB | 32 (virtual) | 125 GB | - |

The GPU nodes are two virtual machines on one server with four P100 cards. Each uses one of the
server's two CPUs (32 logical CPUs) and the memory attached to it, and gets two GPUs passed
through directly. They run Rocky Linux 10, not 9.8 like the compute nodes, so programs built on
the compute nodes may need to be rebuilt for them.

The nodes are connected by 100 Gb/s InfiniBand EDR (Mellanox MT4115 ConnectX-4 cards), a
low-latency network for communication between nodes. More detail: [Koios infrastructure](infrastructure.md).

## Storage and software

Koios has its own home directories, software tree (`/cvmfs/c9.phoebe.lan`) and shared scratch
(`/mnt/shared-scratch`); the project space `/mnt/proj` is the same as on Phoebe. On the compute
nodes each job gets a private `/tmp` on the node's NVMe disk; on the GPU nodes `/tmp` is a local
disk shared by the jobs on that node. The software tree `/cvmfs/c9.phoebe.lan` is not available on
the GPU nodes. See [storage and software](../storage.md).
