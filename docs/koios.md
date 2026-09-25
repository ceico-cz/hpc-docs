---
title: "Koios system description"
wikijs_updated: 2023-11-10
description: "Description of CEICO legacy cluster"
---

# Koios system description

The Koios cluster, a previous-generation system, is composed of 28 compute nodes. Each node is equipped with two 16-core Intel Xeon Skylake CPUs. Moreover, a dedicated node is allocated for GPU-accelerated computing, hosting four high-performance Nvidia Tesla P100 GPUs.

## Accessing Koios

Koios is available using `koios1.fzu.cz` front-end SSH node.
Koios shares the authentication backend with Phoebe, meaning that the same username and SSH key are sufficient for logging in.

## Workload management

Jobs at Koios are managed by the Slurm workload manager, which implements multiple fair-use and priority-queuing algorithms for effective system utilization.

## Hardware

(detailed list of Koios hardware is [here](koios/hw.md))

| Node type | amount | Hostnames   |Processors         | GPUs          | Number of cores (logical CPUs) | Main memory | nvme   |
|-----------|--------|-------------|-------------------|---------------|--------------------------------|-------------|--------|
| compute   | 27     | `n[1-27]`   | 2x [Xeon Gold 6130](koios/hw/Xeon_Gold_6130.md) | -             | 32(64)                         | 384 GB      | 1x 2TB |
| GPU       | 1      | `n28`       | 2x [Xeon Gold 6130](koios/hw/Xeon_Gold_6130.md) | 4x [Tesla P100](koios/hw/p100.md) | 32(64) GPU:4x3584              | 384 GB      | 1x 2TB |

## Interconnect network

The nodes are equipped with MT4115 ConnectX-4 1x100Gb Infiniband EDR cards, ensuring a low-latency network for efficient inter-node communication.

## Storage

### user Home dirs

User homedirs are located at Beegfs[^more_info^](https://www.beegfs.io/c/) cluster filesystem shared with Phoebe.

### Local temporary fast NVME storage

Each node features a ~2TB Intel NVME, mounted as /tmp and accessible as `$TMPDIR`. It's important to note that this storage is non-persistent and undergoes periodic cleaning during node image updates.

### Archive directory

In the `/mnt/archive` directory, slower yet deduplicated and compressed (using VDO [^more_info^](https://www.redhat.com/en/blog/understanding-concepts-behind-virtual-data-optimizer-vdo-rhel-75-beta) ) storage is mounted, serving as an archive for infrequently accessed files

## Software tree

Application software is provided using CVMFS (CernVM File System [^more_info^](https://cernvm.cern.ch/fs/)) in `/cvmfs`. Software is built and organized using Easybuild framework[^more_info^](https://docs.easybuild.io/) utilizing Lmod software modules.
