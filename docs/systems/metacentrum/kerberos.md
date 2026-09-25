---
title: "Passwordless SSH to MetaCentrum with Kerberos"
description: "Get a renewable MetaCentrum Kerberos ticket at desktop login and use it for SSH"
tags:
  - "metacentrum"
  - "kerberos"
---

# Passwordless SSH to MetaCentrum with Kerberos

How to set up a new Ubuntu desktop so it gets a MetaCentrum Kerberos ticket at
login, keeps it renewed automatically, and uses it for passwordless SSH (with
ticket delegation) to the frontend `metafzu.fzu.cz`.

The steps below are for **Kubuntu / KDE Plasma** (the password is kept in KDE
Wallet). If the machine runs **GNOME** (standard Ubuntu), the helper script also
works with GNOME Keyring; the differences are noted where they matter.

You need a [MetaCentrum account](index.md#get-an-account). Throughout this guide, replace
`LOGIN` with your MetaCentrum username.

## Overview

| Piece | Purpose |
|---|---|
| `krb5-user` | MIT Kerberos tools (`kinit`, `klist`, `kdestroy`) |
| `/etc/krb5.conf` | Tells Kerberos where the `META` realm's KDCs are |
| KDE Wallet / GNOME Keyring | Keeps the MetaCentrum password encrypted on disk |
| `~/.local/bin/metacentrum-kinit` | Helper that reads the password from the wallet and gets the **first** ticket |
| `~/.config/autostart/metacentrum-kinit.desktop` | Runs the helper when you log in to the desktop |
| `krb5-auth-dialog` | Background daemon that **renews** the ticket without a password |
| `~/.config/autostart/krb5-auth-dialog.desktop` | Stops the package's own autostart entry from running before the helper |
| `~/.ssh/config` | `metacentrum` host alias with GSSAPI auth and delegation turned on |

What happens at login:

1. The desktop runs the helper through its autostart entry.
2. If a valid ticket already exists, the helper leaves it unchanged.
3. Otherwise, it reads the password from the wallet and pipes it to
   `kinit -f -r 7d LOGIN@META` over stdin. The password never appears in
   command-line arguments, environment variables, or files.
4. The helper starts `krb5-auth-dialog --auto`, which then renews the ticket
   before each expiry.
5. `ssh metacentrum` authenticates with the ticket and delegates a copy of it
   to the frontend, so `qsub`, `qstat`, storage access, and so on work there
   without another password.

## 1. Install packages

```bash
sudo apt install krb5-user krb5-auth-dialog python3-dbus
```

If the installer asks for a default realm, enter `META`. The file is replaced
in the next step anyway, so this answer doesn't matter much.

- For KDE, `python3-dbus` is needed.
- For GNOME, also install `libsecret-tools`, which provides `secret-tool`:

  ```bash
  sudo apt install libsecret-tools
  ```

## 2. Install MetaCentrum's Kerberos configuration

Copy the current `krb5.conf` from the frontend. This is the one time you log
in with your password:

```bash
scp LOGIN@metafzu.fzu.cz:/etc/krb5.conf /tmp/krb5.conf.metacentrum
sudo cp /etc/krb5.conf /etc/krb5.conf.before-metacentrum-$(date +%Y%m%d) 2>/dev/null
sudo install -o root -g root -m 0644 /tmp/krb5.conf.metacentrum /etc/krb5.conf
rm /tmp/krb5.conf.metacentrum
```

Check that it works:

```bash
kinit -f -r 7d LOGIN@META     # asks for your MetaCentrum password
klist -f                      # should show krbtgt/META@META, flags include F and R
```

Flags: `F` means forwardable, which delegation requires. `R` means renewable,
which `krb5-auth-dialog` requires.

## 3. Configure SSH

Add to `~/.ssh/config`:

```sshconfig
Host metacentrum
    User LOGIN
    Hostname metafzu.fzu.cz
    GSSAPIAuthentication yes
    GSSAPIDelegateCredentials yes
    GSSAPIKeyExchange yes
```

!!! warning "Always use the alias"
    SSH matches `Host` against **what you type**, not against the resolved hostname.
    `ssh metacentrum` gets these options. `ssh metafzu.fzu.cz` does **not**: it falls back to
    key or password auth and doesn't delegate a ticket, so `qstat`/`pbsnodes` on the frontend
    then fail with `pbs_gss_establish_context` errors. Alternatively, write
    `Host metacentrum metafzu.fzu.cz` so both names match.

Keep `GSSAPIDelegateCredentials` scoped to this host. Never set it globally.
Anyone with access to the remote side can use a delegated ticket until it
expires.

`GSSAPIKeyExchange` needs Ubuntu's GSSAPI-patched OpenSSH, which is the
default. If your `ssh` reports it as an unknown option, delete that line.

Check it:

```bash
ssh -G metacentrum | grep -Ei '^(user|hostname|gssapiauthentication|gssapidelegatecredentials) '
ssh metacentrum hostname          # no password prompt
ssh metacentrum klist -f          # shows a delegated LOGIN@META ticket
```

## 4. Install the helper script

The helper script is kept in the [site repository](https://github.com/ceico-cz/hpc-docs/blob/main/docs/systems/metacentrum/metacentrum-kinit).
Download it, set your MetaCentrum username in it, and make it executable:

```bash
mkdir -p ~/.local/bin
curl -fsSL -o ~/.local/bin/metacentrum-kinit \
  https://raw.githubusercontent.com/ceico-cz/hpc-docs/main/docs/systems/metacentrum/metacentrum-kinit
sed -i 's/^LOGIN = "LOGIN"/LOGIN = "your-login"/' ~/.local/bin/metacentrum-kinit   # your MetaCentrum username
chmod 0755 ~/.local/bin/metacentrum-kinit
```

The script reads your password, so look through it before you run it
(`less ~/.local/bin/metacentrum-kinit`). It is about 150 lines and needs only Python,
`python3-dbus` (KDE) or `secret-tool` (GNOME), and the Kerberos tools.

Store your password. The script checks it against the MetaCentrum KDC before saving it:

```bash
~/.local/bin/metacentrum-kinit --store
```

On KDE, the wallet may ask you to approve access for `metacentrum-kinit` the
first time. Choose **Always allow**.

Test acquisition from the wallet:

```bash
kdestroy
~/.local/bin/metacentrum-kinit
klist -f
pgrep -af krb5-auth-dialog
```

## 5. Autostart at login

The helper's autostart entry, `~/.config/autostart/metacentrum-kinit.desktop`
(replace `/home/USER` with your home path; autostart `Exec=` lines don't expand
`~`):

```ini
[Desktop Entry]
Type=Application
Name=MetaCentrum Kerberos Ticket
Comment=Acquire a renewable MetaCentrum ticket from the wallet
Exec=/home/USER/.local/bin/metacentrum-kinit
Terminal=false
X-KDE-autostart-after=panel
X-KDE-StartupNotify=false
X-GNOME-Autostart-Delay=5
```

Hide the package's own `krb5-auth-dialog` autostart entry, so it doesn't start
before a ticket exists and prompt for a password. The helper starts it instead.
`~/.config/autostart/krb5-auth-dialog.desktop`:

```ini
[Desktop Entry]
Hidden=true
```

Log out and back in, then check:

```bash
klist -f
pgrep -af krb5-auth-dialog
ssh metacentrum klist -f
```

### Wallet unlock at login

Automation works only if the wallet is unlocked when you log in.

- **KDE:** install `libpam-kwallet5` (or `libpam-kwallet6` on newer releases).
  Use the same password for `kdewallet` as for your login, and choose
  Blowfish, not GPG, for the wallet. SDDM then unlocks it automatically.
- **GNOME:** the login keyring is unlocked by default when its password
  matches your login password.

If the wallet is still locked, you'll get an unlock prompt at login. Accepting
it is fine.

## How renewal works (and when a password is needed again)

```
$ klist -f
Valid starting      Expires             Service principal
25.9.2026 15:12:44  26.9.2026 03:12:44  krbtgt/META@META
        renew until 2.10.2026 12:46:49, Flags: FRAT
```

- **Expires:** the end of the ticket's current lifetime, set by the KDC to a
  few hours. Before then, `krb5-auth-dialog` runs the equivalent of `kinit -R`,
  which needs **no password**.
- **Renew until:** the hard limit, 7 days after the ticket was first issued
  (because of `-r 7d`). After it, the ticket can't be renewed. You then need a
  full `kinit`, which the helper does from the wallet at the next login, or
  when you run it by hand.

If the session runs for more than 7 days, or the ticket expired while the
machine was asleep, run the helper again:

```bash
~/.local/bin/metacentrum-kinit
```

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `ssh -v` shows `Unspecified GSS failure` | Local ticket has expired or is missing. Check `klist -f` and `date`, then run `kinit -R` or the helper. |
| `kinit -R` → `Ticket expired while renewing credentials` | The renewable window has passed too. Run the helper for a full reacquisition. |
| SSH works, but remote `qstat` gives `gss_acquire_cred` errors | No delegation happened. Use `ssh metacentrum`, not the raw hostname. Check with `ssh metacentrum klist -f`. |
| No ticket after login | Run the helper by hand and read its error. Check that the wallet is unlocked and the autostart entry exists. |
| `krb5-auth-dialog` not running | Renewal has stopped silently. Rerun the helper, which starts the daemon again. |
| `kinit: Cannot find KDC for realm "META"` | `/etc/krb5.conf` is missing or wrong. Redo step 2. |
| Password changed at MetaCentrum | Run `~/.local/bin/metacentrum-kinit --store`. |
| Force a Kerberos-only test | `ssh -o PreferredAuthentications=gssapi-with-mic -o PubkeyAuthentication=no -o PasswordAuthentication=no metacentrum hostname` |

## Security notes

- The password is encrypted at rest in the wallet or keyring. The helper passes
  it to `kinit` only over stdin, never as a CLI argument, an environment
  variable, or a plaintext file.
- While the wallet is unlocked, any process running as your desktop user can
  ask for the secret. That's the standard trust model for desktop wallets.
- Limit `GSSAPIDelegateCredentials` to trusted MetaCentrum frontends.
- Upstream reference: [Kerberos in the MetaCentrum documentation](https://docs.metacentrum.cz/en/docs/access/security/kerberos)
