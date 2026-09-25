---
title: "Slurm accounts, QOS and limits"
wikijs_updated: 2025-09-11
description: "The accounts and QOS on Phoebe, and how to add users and limits"
tags:
  - "admin"
  - "slurm"
---

# Slurm accounts, QOS and limits

The state of the Phoebe accounting database in September 2026. Check the current values with
`sacctmgr show qos` and `sacctmgr show assoc`.

## Accounts

All accounts hang directly under `root` with a fair-share weight of 1, and default to the
`normal` QOS.

| Account | Users |
| --- | --- |
| `fzu_a_16` | 8 |
| `fzu_a_29` | 13 |
| `fzu_a_39` | 32 |
| `ext_ceico` | 8 |
| `ext_fzu` | 3 |
| `fzu_project001` | 1 |

!!! warning "TODO"
    Say what each account stands for (FZU divisions? external collaborators of CEICO and of
    FZU?) and which one a new user goes into.

Two associations in `fzu_a_29` have their own group GPU limits: `GrpTRES=gres/gpu=8` and
`GrpTRES=gres/gpu=4`.

## QOS

| QOS | Priority | Per-user limit | Per-job limit | Associations with it as default |
| --- | --- | --- | --- | --- |
| `normal` | 256 | 16 A100 GPUs (`gres/gpu:a100=16`), 3000 running jobs | - | 60 |
| `manyjobs` | 100 | 128 CPUs, 3000 running jobs; flag `OverPartQOS` | - | 1 |
| `newbie` | 500 | 5 running jobs | - | 0 |
| `max400cpu` | 0 | 3000 CPUs | - | 2 |
| `max500cpu` | 0 | **1 CPU** | - | 1 |
| `max64cpu` | 0 | 64 CPUs | - | 0 |
| one per-user QOS (named after its user) | 0 | 128 CPUs | - | 0 |
| `gpu_max2` | 0 | 3 GPUs | 16 CPUs, 3 GPUs, 504 GB | 2 |

!!! note "Names don't match the limits"
    `max400cpu` allows 3000 CPUs, `max500cpu` allows 1 CPU (deliberately) and `gpu_max2`
    allows 3 GPUs. Check the limit, not the name.

In the last 90 days, 20 042 jobs ran with `normal`, 64 with `max400cpu` and 10 with `gpu_max2`.

## Add a user

Create the user in the accounting database and add them to an account:

```
sacctmgr create user name=UserName account=AccountName
```

The user gets the account's default QOS, `normal`.

## Give a user another QOS

Allow the QOS and make it the user's default:

```
sacctmgr modify user name=UserName set qos=max64cpu defaultqos=max64cpu
```

Use `qos+=` instead of `qos=` to add a QOS without removing the others. Jobs already in the
queue keep their old QOS; change them one by one:

```
scontrol update job=123456 qos=max64cpu
```

## Create a QOS with a per-user limit

For example, at most 400 CPUs per user:

```
sacctmgr create qos cpu400
sacctmgr modify qos cpu400 set maxtresperuser=cpu=400
```

## Change the per-user GPU limit

The GPU limit for everyone lives in the `normal` QOS:

```
sacctmgr modify qos normal set maxtresperuser=gres/gpu:a100=16
```
