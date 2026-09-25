---
title: "Storage and software on Phoebe and Koios"
description: "Home directories, local scratch, archive storage and the software tree on the CEICO clusters"
---

# Storage and software on Phoebe and Koios

!!! warning "TODO"
    This page is based on the Koios documentation. Check that each part also applies to Phoebe,
    and add:

    - home directory quotas, and how users can check their usage
    - whether anything is backed up
    - any project or shared scratch storage

## Home directories

Your home directory is on a [BeeGFS](https://www.beegfs.io/c/) cluster file system shared by
Phoebe and Koios, so you see the same files on both clusters.

## Local fast temporary storage

Each compute node has a local NVMe disk mounted as `/tmp` and available to jobs as `$TMPDIR`
(about 2 TB on Koios, 1.7 TB on Phoebe CPU nodes and 3.4 TB on Phoebe GPU nodes). It is much
faster than the shared file system for many small files.

This storage is not persistent: it is cleaned periodically, for example when node images are
updated. Copy results you want to keep back to your home directory before your job ends.

## Archive directory

`/mnt/archive` is slower storage with deduplication and compression
([VDO](https://www.redhat.com/en/blog/understanding-concepts-behind-virtual-data-optimizer-vdo-rhel-75-beta)).
Use it as an archive for files you rarely need.

## Software tree

Application software is provided through [CVMFS](https://cernvm.cern.ch/fs/) (CernVM File
System) in `/cvmfs`. It is built with the [EasyBuild](https://docs.easybuild.io/) framework and
loaded with Lmod [software modules](../software/modules.md).
