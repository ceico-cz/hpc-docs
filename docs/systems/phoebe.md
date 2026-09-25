---
title: "Phoebe"
description: "Phoebe, the current CEICO HPC cluster"
---

# Phoebe

Phoebe is the current CEICO HPC cluster and the main system
for new work. Log in through the front-end node `phoebe.fzu.cz`.

<div class="stats" markdown>

-   **1408** CPU cores
-   **16** NVIDIA A100 GPUs
-   **2 TB** RAM per GPU node
-   **218 TB** shared storage
-   **100 Gb/s** InfiniBand

</div>

## System overview

Phoebe consists of 20 compute nodes, each with 64 CPU cores (2× AMD EPYC 7543[^amd_7543]),
512 GB of RAM and 1.7 TB of fast local NVMe[^wiki_NVME] disk. Two additional *"fat"* GPU nodes
each carry 8 NVIDIA A100[^nvidia_A100] cards, 2 TB of RAM and 3.4 TB of local NVMe storage.

Software, user and project data are stored on 218 TB of hybrid storage built from both solid
state and rotational drives. All components are connected by a low-latency 100 Gbit
InfiniBand fabric. All nodes run Rocky Linux 8.

| pcs | hostnames | resource | n~cores~ | f~cpu~ (base) | f~cpu~ (max) | RAM | local storage | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20  | `n[1-20]` | CPU compute nodes | 64  | 2.8 GHz | 3.7 GHz | 512 GB | 1.7 TB |  -   |
| 2   | `gpu[1-2]` | GPU-accelerated *fat* nodes | 64  | 2.8 GHz | 3.7 GHz | 2 TB | 3.4 TB | 8× NVIDIA A100 |
| 1   | `phoebe.fzu.cz` | login front-end node (virtual machine) | 24 vCPU | 3.5 GHz | 4.0 GHz | 384 GB | -  | AMD EPYC 73F3 host |

More detail: [Phoebe hardware](../hardware.md). If Phoebe helped your research, please
[acknowledge it](../acknowledgement_template.md) in your publications.

## Slurm partitions

Jobs go to the `cpu` partition unless you ask for another one with `--partition`. The
`*_int` partitions are meant for interactive work (see
[interactive session](../slurm/interactive.md)).

| Partition | Nodes | Per node | Time limit | Use |
| --- | --- | --- | --- | --- |
| `cpu` (default) | `n[4-20]` | 64 cores (128 threads), 512 GB | 18 days 8 h | batch CPU jobs |
| `cpu_int` | `n[1-20]` | 64 cores (128 threads), 512 GB | 20 days 10 h | interactive CPU work |
| `gpu` | `gpu[1-2]` | 64 cores, 8× A100 80 GB, 2 TB | 18 days 8 h | batch GPU jobs |
| `gpu1`, `gpu2` | `gpu1` or `gpu2` | as `gpu` | 14 days 4 h | pin a job to one GPU node |
| `gpu_int` | `gpu[1-2]` | as `gpu` | 20 days 10 h | interactive GPU work |
| `small_int` | `s[1-3]` | 8 cores, 64 GB | 7 days 7 h | light interactive work |
| `preempt` | `n[1-20]` | 64 cores (128 threads), 512 GB | 5 days | jobs that may be preempted |

Limits change from time to time; `sinfo` on the login node shows the current values.

## Pictures from the datacenter

<div class="photo-grid" markdown>

![Status LEDs of the compute nodes glowing in the dark server room](../phoebe_pictures/phoebe_realistic_001_small.jpg)
/// caption
Status LEDs in the dark server room
///

![Disk shelves with the storage servers below](../phoebe_pictures/20220526_201547.jpg)
/// caption
Disk shelves and storage servers
///

![Back of the rack with power, Ethernet and InfiniBand cabling](../phoebe_pictures/20220526_201437.jpg)
/// caption
Power, Ethernet and InfiniBand cabling
///

![Front view of the compute nodes](../phoebe_pictures/20230308_130306_2.jpg)
/// caption
Compute nodes, front view
///

</div>

## About the name

![Line drawing of a server](../phoebe_pictures/gj6uq8gm.jpeg){ .plain .off-glb align=right width=140 }

In Greek mythology, Phoebe (*ˈfiːbi*), sister of Κοῖος (Koios), was one of the first
generation of Titans, the sons and daughters of Uranus and Gaia.[^wiki_Phoebe]
Koios is also the name of our [previous cluster](../koios.md).

[^amd_7543]: [AMD EPYC™ 7543, vendor product page](https://www.amd.com/en/products/cpu/amd-epyc-7543)
[^wiki_NVME]: [Wikipedia: NVMe](https://en.wikipedia.org/wiki/NVM_Express)
[^nvidia_A100]: [NVIDIA A100, vendor product page](https://www.nvidia.com/en-us/data-center/a100/)
[^wiki_Phoebe]: [Wikipedia: Phoebe (Titaness)](https://en.wikipedia.org/wiki/Phoebe_(Titaness))
