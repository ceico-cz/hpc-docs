---
title: "Accessing Phoebe and Koios using SSH from macOS"
wikijs_updated: 2022-09-06
---

# Accessing Phoebe and Koios using SSH from macOS

!!! info "Note"
    Before first login, you need to [activate your account](../getting-a-user-account.md). The same account works on Phoebe and Koios.

## Access the SSH front-end node

One can use Secure Shell protocol (SSH) to access the front-end nodes of Phoebe and Koios.

SSH client is built-in in all contemporary Apple operating systems.

To access the Phoebe or Koios login node, use one of these commands:

```
ssh <username>@phoebe.fzu.cz     # Phoebe
ssh <username>@koios1.fzu.cz     # Koios
```

where `<username>` is your FZU "Kerberos" account.

To access system, we use exclusively Public Key Authentication.

## Make SSH login more comfortable

To make ssh connection faster, you might decide to create `~/.ssh/config` file with an entry for each cluster. Make sure to replace the `<username>` template with your FZU username.

```
Host phoebe
        Hostname phoebe.fzu.cz
        User <username>

Host koios
        Hostname koios1.fzu.cz
        User <username>
```

Once this host definition is created, it is enough to just type `ssh phoebe` or `ssh koios` to get to the cluster.
