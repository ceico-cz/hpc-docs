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

Save as `~/.local/bin/metacentrum-kinit` and edit `LOGIN` at the top:

```python
#!/usr/bin/python3
"""Obtain a renewable MetaCentrum Kerberos ticket using a password kept in
KDE Wallet (Plasma) or the Secret Service keyring (GNOME), then start
krb5-auth-dialog to keep the ticket renewed.

Usage:
  metacentrum-kinit           get a ticket if none is valid, start monitor
  metacentrum-kinit --store   validate a password with the KDC, then save it
"""
import getpass
import os
import shutil
import subprocess
import sys
import tempfile

LOGIN = "LOGIN"                      # <-- your MetaCentrum username
PRINCIPAL = f"{LOGIN}@META"
APP_ID = "metacentrum-kinit"
KW_FOLDER = "Passwords"
KW_ENTRY = f"MetaCentrum {PRINCIPAL}"
SECRET_ATTRS = ["service", "metacentrum-kerberos", "principal", PRINCIPAL]


# ---------- KDE Wallet backend (native D-Bus API) ----------

def kwallet():
    import dbus
    bus = dbus.SessionBus()
    for svc, path in (("org.kde.kwalletd6", "/modules/kwalletd6"),
                      ("org.kde.kwalletd5", "/modules/kwalletd5")):
        try:
            iface = dbus.Interface(bus.get_object(svc, path), "org.kde.KWallet")
            iface.localWallet()
        except dbus.DBusException:
            continue
        handle = int(iface.open(str(iface.localWallet()), dbus.Int64(0), APP_ID))
        if handle < 0:
            raise RuntimeError("KDE Wallet could not be opened")
        return iface, handle
    return None


def kwallet_read(kw):
    iface, h = kw
    return str(iface.readPassword(h, KW_FOLDER, KW_ENTRY, APP_ID))


def kwallet_write(kw, password):
    iface, h = kw
    if not bool(iface.hasFolder(h, KW_FOLDER, APP_ID)):
        iface.createFolder(h, KW_FOLDER, APP_ID)
    if int(iface.writePassword(h, KW_FOLDER, KW_ENTRY, password, APP_ID)) != 0:
        return False
    return kwallet_read(kw) == password


# ---------- Secret Service backend (GNOME Keyring via secret-tool) ----------

def secret_read():
    r = subprocess.run(["secret-tool", "lookup", *SECRET_ATTRS],
                       capture_output=True, text=True, check=False)
    return r.stdout.rstrip("\n") if r.returncode == 0 else ""


def secret_write(password):
    r = subprocess.run(["secret-tool", "store", "--label", KW_ENTRY, *SECRET_ATTRS],
                       input=password, text=True, check=False)
    return r.returncode == 0 and secret_read() == password


def backend():
    """Prefer KDE Wallet on Plasma, otherwise the Secret Service."""
    if "KDE" in os.environ.get("XDG_CURRENT_DESKTOP", ""):
        try:
            kw = kwallet()
            if kw:
                return ("kwallet", kw)
        except Exception as e:
            print(f"KDE Wallet unavailable: {e}", file=sys.stderr)
    if shutil.which("secret-tool"):
        return ("secret", None)
    raise RuntimeError("No usable password store (KDE Wallet or secret-tool)")


def read_password(be):
    return kwallet_read(be[1]) if be[0] == "kwallet" else secret_read()


def write_password(be, password):
    return kwallet_write(be[1], password) if be[0] == "kwallet" else secret_write(password)


# ---------- Kerberos ----------

def run_kinit(password, cache_name=None):
    env = os.environ.copy()
    if cache_name:
        env["KRB5CCNAME"] = cache_name
    return subprocess.run(["kinit", "-f", "-r", "7d", PRINCIPAL],
                          input=password + "\n", text=True, env=env,
                          check=False).returncode


def start_monitor():
    running = subprocess.run(["pgrep", "-f", "(^|/)krb5-auth-dialog( |$)"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             check=False).returncode == 0
    if not running:
        subprocess.Popen(["krb5-auth-dialog", "--auto"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)


def store_password():
    password = getpass.getpass(f"Password for {PRINCIPAL} (validate, then save): ")
    with tempfile.TemporaryDirectory(prefix="metacentrum-krb5-") as d:
        if run_kinit(password, f"FILE:{d}/ccache") != 0:
            print("MetaCentrum rejected that password; nothing was saved.", file=sys.stderr)
            return 1
    if not write_password(backend(), password):
        print("Saving the password to the wallet failed.", file=sys.stderr)
        return 1
    print("Password validated and saved.")
    return 0


def acquire_ticket():
    if subprocess.run(["klist", "-s"], check=False).returncode == 0:
        start_monitor()
        return 0
    password = read_password(backend())
    if not password:
        print(f"No password for {PRINCIPAL} in the wallet; run with --store.",
              file=sys.stderr)
        return 1
    result = run_kinit(password)
    password = ""
    if result == 0:
        start_monitor()
    return result


if __name__ == "__main__":
    if sys.argv[1:] == ["--store"]:
        raise SystemExit(store_password())
    if len(sys.argv) == 1:
        raise SystemExit(acquire_ticket())
    print(f"Usage: {sys.argv[0]} [--store]", file=sys.stderr)
    raise SystemExit(2)
```

Make it executable and store the password. The script checks the password
against the MetaCentrum KDC before saving it:

```bash
chmod 0755 ~/.local/bin/metacentrum-kinit
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
