---
title: "Mount storage over SSH using sshfs"
wikijs_updated: 2023-11-15
---

# Mount storage over SSH using sshfs

To exchange data quickly between your laptop and our clusters, you can mount your cluster
home directory on your laptop or workstation with sshfs. It then behaves like a local
folder. Phoebe and Koios have separate home directories; the examples below mount your Phoebe
home.

## Prerequisites

* configured [key-based authentication](ssh-key.md)
* a `phoebe` host entry in `~/.ssh/config`, as described in [SSH](ssh.md):

```
Host phoebe
        Hostname phoebe.fzu.cz
        User <username>
```

## Create mount aliases

=== "Linux"

    Into your local `~/.bashrc` (if you use bash), insert this snippet. Replace `johndoe`
    with your cluster username.

    ```
    phoebe_username='johndoe'

    alias mount_phoebe="mkdir -p ~/phoebe_mount && sshfs -o reconnect,ServerAliveInterval=2,ServerAliveCountMax=3 phoebe:/home/${phoebe_username} ~/phoebe_mount"
    alias umount_phoebe='fuser -Mk ~/phoebe_mount; fuser -Mk ~/phoebe_mount; fuser -Mk ~/phoebe_mount;  fusermount -u ~/phoebe_mount'
    ```

    Load the changed `~/.bashrc`:

    ```
    source ~/.bashrc
    ```

=== "macOS"

    sshfs on macOS needs [macFUSE](https://macfuse.github.io/) and its sshfs package.

    Open `~/.zshrc` in your favorite editor (or create it when missing) and insert this
    snippet. Replace `johndoe` with your cluster username.

    ```
    phoebe_username='johndoe'

    alias mount_phoebe="mkdir -p ~/phoebe_mount && sshfs -o reconnect,ServerAliveInterval=2,ServerAliveCountMax=3 phoebe:/home/${phoebe_username} ~/phoebe_mount"
    alias umount_phoebe='umount ~/phoebe_mount'
    ```

    To make sure that `~/.zshrc` is loaded in every new shell, edit `~/.zprofile` and insert:

    ```
    [[ -s ~/.zshrc ]] && source ~/.zshrc
    ```

## Mount and unmount

In a new shell, type `mount_phoebe` to mount your cluster home directory into
`~/phoebe_mount`. Type `umount_phoebe` to unmount it.
