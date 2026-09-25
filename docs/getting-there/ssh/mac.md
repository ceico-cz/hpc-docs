---
title: "Acessing Phoebe system using SSH from Mac"
wikijs_updated: 2022-09-06
---

# Acessing Phoebe system using SSH from Mac

!!! info "Note"
    Before first login, initial [activating Phoebe account](../getting-a-user-account.md) is necessary.

## Accessing SSH front-end node

One can use Secure Shell protocol (SSH) to access front-end nodes of Phoebe HPC system.

SSH client is built-in in all contemporary Apple operating systems.

To access Phoebe login node use following command:

```
ssh <username>@phoebe.fzu.cz
```

where `<username>` is your FZU "Kerberos" account.

To access system, we use exclusively Public Key Authentication.

## making ssh login more comfortable

To make ssh connection faster, you might decide to create `~/.ssh/config` file with an Phoebe entry. Make sure to replace `<username>`template with your FZU/Phoebe username.

```
Host phoebe
        Hostname phoebe.fzu.cz
        User <username>
```

Once this host definition is created, it is enough to just type `ssh phoebe` to get to our cluster.
