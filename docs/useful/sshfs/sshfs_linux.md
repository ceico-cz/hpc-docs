---
title: "Mount remote directories using sshfs at Linux laptop/workstation"
wikijs_updated: 2023-11-15
---

# Mount remote directories using sshfs at Linux laptop/workstation

## Prerequisites

* configured [key-based authentication](../../getting-a-user-account/create-ssh-keypair-nix.md)
* `.ssh/config` with Koios/Phoebe front-end node configuration example:

```
Host koios1
  Hostname koios1.fzu.cz
  User johndoe
```

## ~/.bashrc modification

Into your local `~/.bashrc` (if you use bash), insert this snippet. Replace `johndoe` with your real koios username.

```
koios_username='johndoe'

k1_alias="koios1"

alias mount_koios1="mkdir -p ~/koios_mount && sshfs -o reconnect,ServerAliveInterval=2,ServerAliveCountMax=3 ${k1_alias}:/home/${koios_username} ~/koios_mount"
alias umount_koios='fuser -Mk ~/koios_mount; fuser -Mk ~/koios_mount; fuser -Mk ~/koios_mount;  fusermount -u ~/koios_mount'
```

## Result

If everything went fine, after loading changed `~/.bashrc` by typing

```
source ~/.bashrc
```

you can mount remote by typing bash alias `mount_koios1` in your shell should mount your koios_home into `~/koios_mount`.
