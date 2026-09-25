---
title: "CUDA driver and toolkit"
wikijs_updated: 2024-01-29
description: "NVIDIA driver and CUDA on the Phoebe GPU nodes: current state and how to update"
tags:
  - "admin"
  - "cuda"
---

# CUDA driver and toolkit

## Current state

Checked on `gpu2` in September 2026:

| Component | Version |
| --- | --- |
| Operating system | Rocky Linux 8.10, kernel `4.18.0-553.162.1.el8_10` |
| GPUs | 8× NVIDIA A100-SXM4-80GB, MIG disabled |
| NVIDIA driver | `615.71.09`, open kernel module (`kmod-nvidia-open-dkms`), with `nvidia-fabricmanager` |
| Highest CUDA version the driver supports | 13.4 |
| CUDA toolkits installed on the node | 13.2, 13.3, 13.4 |

Users get CUDA from the `system` module stack (`/cvmfs/system.phoebe.lan`): `CUDA/11.4.1`,
`11.7.0`, `12.2.0`, `12.6.0`, `12.8.1`, `12.9.1`, `13.0.2` and `13.3.0`, plus
`NVHPC/24.9-CUDA-12.6.0` in the `2024a` stack. The driver runs all of them.

!!! warning "TODO"
    Check `gpu1` too; it was down when this page was updated.

## Choose versions

NVIDIA's [framework support matrix](https://docs.nvidia.com/deeplearning/frameworks/support-matrix/index.html)
lists which driver and CUDA version each NGC container release needs. A newer driver runs
applications built for older CUDA versions, so update the driver first.

## Update the driver

The driver comes from NVIDIA's CUDA repository for RHEL 8 as a `dnf` module stream. Drain the
node first (see [Slurm admin snippets](slurm-snippets.md#drain-and-resume-a-node)), list the
available streams, and switch to the one you want (the nodes use the open kernel module):

```
dnf module list nvidia-driver
dnf -y module reset nvidia-driver
dnf -y module install nvidia-driver:<stream>
```

Keep `nvidia-fabricmanager` at exactly the same version as the driver; the A100-SXM4 nodes
need it for NVLink. Reboot to load the new driver, check it with `nvidia-smi`, and resume the
node.

## Install a CUDA toolkit on the node

```
dnf -y install cuda-toolkit-13-4
```

Toolkits for users are better provided as modules in the software tree, so that each user
can choose a version.

## History

In January 2024 the nodes ran driver 545 with CUDA 12.3.2, installed from the local RPM
repository `cuda-repo-rhel8-12-3-local-12.3.2_545.23.08-1` and the `nvidia-driver:545-dkms`
module stream.
