---
title: "Acessing Phoebe system using SSH from Linux"
wikijs_updated: 2023-11-16
---

# Acessing Phoebe system using SSH from Linux

!!! info "Note"
    Before first login, initial [activating Phoebe account](../getting-a-user-account.md) is necessary.

## Accessing SSH front-end node

One can use Secure Shell protocol (SSH) to access front-end nodes of Phoebe HPC system.

SSH client is built-in in all contemporary Linux distributions.

To access Phoebe login node use following command:

```shell
ssh <username>@phoebe.fzu.cz
```

where `<username>` is your FZU "Kerberos" account.

To access system, we use exclusively Public Key Authentication.

## making ssh login more comfortable

To make ssh connection faster, you might decide to create `~/.ssh/config` file with an Phoebe entry. Make sure to replace `<username>`template with your FZU/Phoebe username.

```shell
Host phoebe
        Hostname phoebe.fzu.cz
        User <username>
```

Once this host definition is created, it is enough to just type `ssh phoebe` to get to our cluster.
