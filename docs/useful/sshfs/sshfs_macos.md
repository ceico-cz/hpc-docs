---
title: "Mount sshfs on MacOs"
wikijs_updated: 2023-11-15
---

# Mount sshfs on MacOs

## Create mount alias in `~/.zshrc`

Open file `~/.zshrc` in your favorite editor (or create it when missing) and insert this snippet:

```
phoebe_username='your username'


alias mount_phoebe="mkdir -p ~/phoebe_mount && sshfs -o reconnect,ServerAliveInterval=2,ServerAliveCountMax=3 phoebe.fzu.cz:/home/${phoebe_username} ~/phoebe_mount"
alias umount_koios='umount ~/phoebe_mount'
```

To make sure that `~/.zshrc` is loaded in new shell instance, edit `.zprofile` and insert:

```
[[ -s ~/.zshrc ]] && source ~/.zshrc

```

If the process executed successfully, entering the command alias `mount_phoebe` in your shell ought to seamlessly mount your home directory to `~/phoebe_mount` within your local home directory.
