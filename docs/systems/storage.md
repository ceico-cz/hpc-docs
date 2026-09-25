---
title: "Storage and software on Phoebe and Koios"
description: "Home directories, project space, local scratch and the software tree on the CEICO clusters"
---

# Storage and software on Phoebe and Koios

| What | Path | Phoebe | Koios |
| --- | --- | --- | --- |
| Home directory | `~` (`/home/<username>`) | own home directory | own home directory, separate from Phoebe's |
| Project space | `/mnt/proj/<project>` | yes | yes, the same directories |
| Local scratch | `/tmp` on the compute node | shared by the jobs on a node | private to each job |
| Shared scratch | `/mnt/shared-scratch` | - | yes |
| Software | `/cvmfs/...` | `2023a` to `2026a` and `system` stacks | its own stack, `c9` |

!!! warning "TODO"
    Add home directory quotas and how users can check their usage, whether anything is backed
    up, how to get project space, and what `/mnt/shared-scratch` on Koios is for.

## Home directories

Both clusters keep home directories on the same [BeeGFS](https://www.beegfs.io/c/) storage
(218 TB), but **each cluster has its own home directory**: files you create on Phoebe don't
appear on Koios, and the other way round. To move files between the clusters, copy them, for
example with `rsync` over SSH.

Your account and SSH key are the same on both clusters.

## Project space

`/mnt/proj` holds one directory per project, named `pNNN_<name>`, on both clusters. A project
directory belongs to the project's own group, and only its members can read and write it. New
files and directories inside it get the project group automatically, so the whole project can
use them.

The project space is 1 TB in total and is shared by all projects.

## Local temporary storage

Each compute node has a local NVMe disk for temporary files, much faster than the shared file
systems for many small files. Copy results you want to keep to your home directory or project
space before your job ends.

=== "Phoebe"

    `/tmp` is on the node's NVMe disk: 1.7 TB on the CPU nodes, 3.2 TB on the GPU nodes and
    about 1 TB on the small nodes. It is shared by all jobs on the node, and files are not
    removed when a job ends; the system deletes files in `/tmp` that haven't been used for 10
    days. `$TMPDIR` is not set.

    Use a directory of your own and remove it at the end of the job:

    ```shell
    export TMPDIR=/tmp/$USER/$SLURM_JOB_ID
    mkdir -p "$TMPDIR"
    # ... your work ...
    rm -rf "$TMPDIR"
    ```

=== "Koios"

    Each job gets its own private `/tmp` on the node's NVMe disk (1.7 TB per node, shared by the
    jobs on the node). Other jobs don't see it, and it is deleted when the job ends.

## Software tree

Application software comes from [CVMFS](https://cernvm.cern.ch/fs/) (CernVM File System) under
`/cvmfs`. It is built with the [EasyBuild](https://docs.easybuild.io/) framework and loaded with
Lmod [software modules](../software/modules.md). The two clusters have different trees:

* **Phoebe**: the stacks `2023a` to `2026a` and `system`, under `/cvmfs/<stack>.phoebe.lan`.
* **Koios**: its own tree, `/cvmfs/c9.phoebe.lan`.
