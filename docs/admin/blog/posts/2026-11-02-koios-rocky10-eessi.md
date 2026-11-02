---
title: "Koios: Rocky Linux 10 and EESSI only"
date: 2026-11-02
slug: koios-rocky10-eessi
---

# Koios: Rocky Linux 10 and EESSI only

The Koios login node `koios1.fzu.cz` runs Rocky Linux 10 since 30 October 2026, and 18 of the 27
compute nodes since 2 November. All software modules on Koios now come from the
[EESSI software stack](../../../software/eessi.md); the former Koios module tree
`/cvmfs/c9.phoebe.lan` has been retired.

<!-- more -->

## What changes for you

* **Start EESSI** before loading modules, in each shell and at the start of each job script:

    ```shell
    source /cvmfs/software.eessi.io/versions/2025.06/init/lmod/bash
    module load foss/2024a
    ```

    Without it, `module avail` shows nothing. See [Software modules](../../../software/modules.md#koios).
* **Rebuild** programs and Python environments that used `c9` modules. EESSI has the same
  `foss` toolchains and far more software; `HEALPix`, `PFFT` and `VTune` have no EESSI module.
* **Partitions**: the default partition `cpu` now holds the Rocky Linux 10 compute nodes; use it
  for batch and interactive work. The new partition `legacy` keeps the eight nodes that still run
  Rocky Linux 9.8 until they are reinstalled. `cpu_int`, `rocky10` and the short-lived
  `rocky10_cpu` were removed, `preempt` is closed. See
  [Koios](../../../systems/koios/index.md#slurm-partitions).
* The Apptainer images in `/cvmfs/apptainer.phoebe.lan` are now available on Koios too.

Home directories, `/mnt/shared-scratch` and `/mnt/proj` are unchanged.
