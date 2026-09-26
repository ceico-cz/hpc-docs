---
title: "Koios: private per-job /tmp on the local NVMe"
date: 2026-07-30
slug: koios-per-job-tmp
---

# Koios: private per-job /tmp on the local NVMe

Since 30 July 2026 every job on the Koios compute nodes gets its own `/tmp`, on the node's NVMe
disk, that no other job can see and that is removed when the job ends.

<!-- more -->

## How it is set up

The change in `slurm.conf` on `slurmserver2.koios` was one line (`PrologFlags=contain` was
already set):

```
NamespaceType=namespace/linux
```

The plugin is configured in `/etc/slurm/namespace.yaml` (last edited on 10 August 2026):

```yaml
defaults:
  base_path: "none"
node_confs:
  - nodes: ["n1", "n2", ..., "n27"]   # shortened: the file lists n1 to n27 one per line
    options:
      auto_base_path: false
      base_path: "/mnt/.nvme"
      dirs: "/tmp"
      shared: true
```

* `base_path: "/mnt/.nvme"`: on each node, the 1.7 TB NVMe volume `vg0-tmp` is mounted at
  `/mnt/.nvme`. Each job gets a directory `/mnt/.nvme/<jobid>`.
* `dirs: "/tmp"`: that directory is mounted as `/tmp` inside the job's own mount namespace, so
  the job sees only its own files.
* `shared: true`: mounts made on the node after the job starts (for example by autofs) still
  propagate into the job's namespace.
* `defaults: base_path: "none"`: nodes not listed (the login and small nodes) keep a normal
  `/tmp`.

When the job ends, Slurm removes `/mnt/.nvme/<jobid>` and everything in it. On a node,
`findmnt | grep /mnt/.nvme` lists the directories of the running jobs.

## Phoebe

Phoebe does not use a namespace plugin (`NamespaceType` is unset). `/tmp` on its nodes is one
NVMe partition shared by all jobs, and the only cleanup is the standard `systemd-tmpfiles`
rule that deletes files not used for 10 days. Users are told to use `/tmp/$USER/$SLURM_JOB_ID`
and remove it themselves; see [storage and software](../../../systems/storage.md).

!!! warning "TODO"
    Say whether Phoebe should get the same setup, and why it was introduced on Koios first.
