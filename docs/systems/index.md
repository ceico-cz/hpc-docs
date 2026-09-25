---
title: "Systems"
description: "Compute systems available to members of the CEICO project"
---

# Systems

CEICO members can use two in-house clusters at the Institute of Physics (FZU) and several
third-party systems operated by other providers.

## CEICO clusters

Phoebe and Koios share user accounts and SSH keys, so one account works on
both. Both use the [Slurm](../slurm/index.md) workload manager. See
[storage and software](storage.md) for where your files live.

| System | Status | Login node | CPU cores | GPUs | Details |
| --- | --- | --- | --- | --- | --- |
| **Phoebe** | current | `phoebe.fzu.cz` | 1408 (AMD EPYC 7543) | 16× NVIDIA A100 | [Overview](phoebe/index.md) · [Hardware](phoebe/hardware.md) |
| **Koios** | legacy | `koios1.fzu.cz` | 864 (Intel Xeon Gold 6130) | 4× NVIDIA Tesla P100 (currently dedicated to a project) | [Overview](koios/index.md) · [Hardware](koios/hardware.md) |

## Third-party systems

These systems are run by other institutions. They have their own accounts, rules and user
documentation; the pages here cover only what is specific to CEICO users.

| System | Operator | Pages on this site |
| --- | --- | --- |
| **MetaCentrum** | CESNET, Czech national grid infrastructure | [Overview](metacentrum/index.md) · [Kerberos SSH](metacentrum/kerberos.md) · [HyperQueue](metacentrum/hyperqueue.md) |
