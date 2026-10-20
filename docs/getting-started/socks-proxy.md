---
title: "Poor man's VPN over SSH"
wikijs_updated: 2023-11-15
---

# Poor man's VPN over SSH

!!! info "FZU account required"
    This uses the institute SSH server `limba.fzu.cz`, so you need an FZU institute account
    (your main e-mail username and Kerberos password), not just a Phoebe account.

Using traffic tunneling over a SOCKS tunnel, especially through SSH, offers several benefits, like security, encryption and posibility to access services available from FZU internal networks only.

To configure Firefox to tunnel traffic over a SOCKS tunnel created by SSH, you can follow these steps:

## Create an SSH tunnel

Open a terminal or command prompt on your local machine and use the following command to create an SSH tunnel with dynamic port forwarding:

```bash
ssh -D 1080 user@limba.fzu.cz
```

Replace user with your main (email) institute username, log in with your Kerberos password.

## Configure Firefox

Open Firefox and follow these steps:

### Open the preferences
        
- On Windows and Linux, click on the three horizontal lines in the top-right corner, then select "Options."
- On macOS, click on "Firefox" in the menu bar, then select "Preferences."

### Go to network settings

- In the Preferences/Options page, select "General" on the left sidebar, scroll down to the "Network Settings" section.

### Configure proxy settings

- Click on the "Settings..." button next to "Connection."
- In the Connection Settings window, choose the "Manual proxy configuration" option

### Enter the SOCKS host

- In the "SOCKS Host" field, enter localhost as the host and `1080` as the port (or the port you specified in the SSH command).

### Select SOCKS v5

- Choose "SOCKS v5" as the type of proxy.

### Configure "No proxy for"

- You may want to add `localhost, 127.0.0.1` to the "No Proxy for" field to prevent the SSH tunnel itself from being proxied.

### Click OK

- Click "OK" to save the changes and close the Connection Settings window.

## Screenshot: Firefox

![Firefox connection settings with a manual SOCKS5 proxy on localhost](../screenshots/socks5_firefox.png)

## System-wide configuration on macOS

![macOS network proxy settings with a SOCKS proxy on 127.0.0.1](../screenshots/screenshot_mac.png)

## Keep the tunnel open with autossh (Linux)

The tunnel closes when the SSH session ends, for example when your laptop sleeps or the Wi-Fi
drops. On Linux with systemd, autossh can keep it open and restart it for you. It needs
[key-based login](ssh-key.md) to limba, since nobody is there to type a password.

Install autossh, for example `sudo apt install autossh` on Debian and Ubuntu or
`sudo dnf install autossh` on Fedora. Then create the file
`~/.config/systemd/user/autossh-limba.service`, replacing `user` with your institute
username:

```ini
[Unit]
Description=SOCKS tunnel to limba.fzu.cz

[Service]
ExecStart=/usr/bin/autossh -M 0 -N -D 1080 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 user@limba.fzu.cz
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

Start it now and at every login:

```bash
systemctl --user daemon-reload
systemctl --user enable --now autossh-limba
```

`systemctl --user status autossh-limba` shows whether the tunnel is running. The proxy is
then always available on `localhost:1080`.
