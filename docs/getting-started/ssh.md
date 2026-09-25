---
title: "Connect to Phoebe and Koios with SSH"
wikijs_updated: 2025-10-13
---

# Connect to Phoebe and Koios with SSH

!!! info "Note"
    Before your first login, you need an [account](account.md). The same account and SSH key
    work on Phoebe and Koios.

You reach each cluster through its front-end (login) node: `phoebe.fzu.cz` for Phoebe and
`koios1.fzu.cz` for Koios. Your username is your FZU "Kerberos" username, usually the part of
your e-mail address before `@`. Only SSH key logins are accepted.

![Users reach the phoebe.fzu.cz front-end node over the internet; compute and GPU nodes and shared storage sit behind it on the cluster network](internet_phoebe_access.png)
/// caption
How you reach Phoebe: everything goes through the front-end node `phoebe.fzu.cz`.
///

## Connect

=== "Linux / macOS"

    The SSH client is built into Linux and macOS. Open a terminal and run one of:

    ```shell
    ssh <username>@phoebe.fzu.cz     # Phoebe
    ssh <username>@koios1.fzu.cz     # Koios
    ```

    To make this shorter, create `~/.ssh/config` with an entry for each cluster. Replace
    `<username>` with your FZU username.

    ```shell
    Host phoebe
            Hostname phoebe.fzu.cz
            User <username>

    Host koios
            Hostname koios1.fzu.cz
            User <username>
    ```

    Then `ssh phoebe` or `ssh koios` is enough.

=== "Windows (MobaXterm)"

    We recommend [MobaXterm](https://mobaxterm.mobatek.net/download.html), a terminal with a
    built-in SSH client and X server. Create a profile for Phoebe:

    1. Click ++"Session"++ and then ++"SSH"++.
    2. Fill in the remote host as `phoebe.fzu.cz`.
    3. Tick ++"Specify username"++ and fill in your FZU username.
    4. Click "Advanced SSH settings".
    5. Tick ++"Use private key"++ and select your private key (`.ppk`) file.
    6. Click ++"OK"++.

    For Koios, create a second profile the same way with the remote host `koios1.fzu.cz`.

    To connect, click the profile in the left column. A console window opens.

    Windows 10 and 11 also include an OpenSSH client: the `ssh` commands from the Linux / macOS
    tab work in PowerShell with a key created by `ssh-keygen`.

## Check the host key on first connection

The first time you connect, SSH shows the server's key fingerprint and asks whether to trust it.
Continue only if it matches the one below:

| Host | ED25519 key fingerprint |
| --- | --- |
| `phoebe.fzu.cz` | `SHA256:xy6+Upes9O4LWWQkME7TjWsmotoTOMlZMSBBWg+j2Zk` |
| `koios1.fzu.cz` | `SHA256:iIOuILdupxCyIhkFKNjlsRP1hs/cFHvuBKu9XF8HVFQ` |
| `koios2.fzu.cz` | `SHA256:iwY/4d72sj+3KK5Mh5NgpcqJangwPK5GAIUYTm5i7Hw` |
