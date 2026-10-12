---
title: "Short SSH host aliases"
description: "Use ~/.ssh/config to give remote hosts short names and the right remote username"
---

# Short SSH host aliases

Typing `ssh jnovak@phoebe.fzu.cz` gets tedious, and it is easy to forget the username part.
Without it, SSH logs in with your **local** username, the one you have on your laptop. If that
differs from your account on the cluster (for example `jan` on the laptop and `jnovak` on
Phoebe), the login fails with `Permission denied` even though your key is fine.

An entry in `~/.ssh/config` on your laptop or workstation fixes both problems: it gives the host
a short name (an alias) and remembers which username to use there.

## Set up the aliases

Create or edit `~/.ssh/config` and add one block per host. Replace `<fzu-username>` with your
FZU username and `<meta-login>` with your MetaCentrum login, which may be different:

```sshconfig
# Phoebe
Host phoebe
    HostName phoebe.fzu.cz
    User <fzu-username>

# Koios
Host koios
    HostName koios1.fzu.cz
    User <fzu-username>

# MetaCentrum frontend at FZU
Host metafzu
    HostName metafzu.fzu.cz
    User <meta-login>
```

What the keywords mean:

| Keyword | Meaning |
| --- | --- |
| `Host` | the alias, the name you type after `ssh`; it can be anything you like |
| `HostName` | the real name (or IP address) of the server |
| `User` | the username on that server, used instead of your local one |

SSH refuses a config file that other users can write to, so keep it private:

```shell
chmod 600 ~/.ssh/config
```

Now these commands are enough:

```shell
ssh phoebe
ssh koios
ssh metafzu
```

!!! tip "Windows"
    The OpenSSH client built into Windows 10 and 11 reads the same file, at
    `C:\Users\<you>\.ssh\config`. MobaXterm keeps its own session profiles instead; see
    [SSH](../getting-started/ssh.md).

## The alias works everywhere SSH does

Every tool built on SSH reads `~/.ssh/config`, so the alias also works for copying files and
for other programs:

```shell
scp results.tar.gz phoebe:                 # copy to your Phoebe home
scp koios:job/output.log .                 # copy from Koios
rsync -av data/ metafzu:project/data/      # sync a directory to MetaCentrum
sshfs phoebe: ~/phoebe_mount               # mount your Phoebe home, see "sshfs"
```

VS Code's Remote-SSH extension also lists the aliases from this file. Mounting with sshfs is
described in [Mount storage over SSH](../getting-started/sshfs.md).

## Check what SSH will do

`ssh -G` prints the settings SSH would use for a name, without connecting. Use it to confirm
that the alias picks up the right host and user:

```shell
ssh -G koios | grep -E '^(hostname|user) '
```

```
hostname koios1.fzu.cz
user jnovak
```

## Good to know

* **The alias matches only what you type.** `ssh phoebe` uses the block above, but
  `ssh phoebe.fzu.cz` does not, and logs in with your local username again. If you want both
  names to work, list them both: `Host phoebe phoebe.fzu.cz`.
* **The first match wins.** For each keyword, SSH uses the first value it finds. Put specific
  `Host` blocks at the top and general defaults in a `Host *` block at the end of the file.
* **A non-default key.** If your cluster key is not one of the default files (such as
  `~/.ssh/id_ed25519`), add `IdentityFile ~/.ssh/<key-file>` to the block. See
  [SSH key](../getting-started/ssh-key.md).
* **MetaCentrum without passwords.** To log in to `metafzu.fzu.cz` with a Kerberos ticket and
  have `qsub`/`qstat` work there, the alias needs a few more lines; see
  [Passwordless SSH to MetaCentrum with Kerberos](../systems/metacentrum/kerberos.md).
* **Keep idle connections open.** If your connection drops after a while of inactivity, add
  `ServerAliveInterval 60` to the block (or to `Host *`), so SSH sends a keep-alive message
  every minute.

The full list of keywords is in `man ssh_config`, also available
[online](https://man.openbsd.org/ssh_config).
