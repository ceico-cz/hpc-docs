---
title: "Systems"
description: "Compute systems available to members of the CEICO project"
---

# Systems

CEICO members can use two in-house clusters at the Institute of Physics (FZU) and several
third-party systems operated by other providers.

## CEICO clusters

Phoebe and Koios share user accounts, SSH keys and home directories, so one account works on
both. Both use the [Slurm](../slurm.md) workload manager.

| System | Status | Login node | CPU cores | GPUs | Details |
| --- | --- | --- | --- | --- | --- |
| **Phoebe** | current | `phoebe.fzu.cz` | 1408 (AMD EPYC 7543) | 16× NVIDIA A100 | [Overview](phoebe.md) · [Hardware](../hardware.md) |
| **Koios** | legacy | `koios1.fzu.cz` | 864 (Intel Xeon Gold 6130) | – | [Overview](../koios.md) · [Hardware](../koios/hw.md) |

## Third-party systems

These systems are run by other institutions. They have their own accounts, rules and user
documentation; the pages here cover only what is specific to CEICO users.

| System | Operator | Pages on this site |
| --- | --- | --- |
| **MetaCentrum** | CESNET, Czech national grid infrastructure | [Overview](metacentrum/index.md) · [Kerberos SSH](metacentrum/kerberos.md) · [HyperQueue](../metacentrum/hq_at_metacentrum.md) |
