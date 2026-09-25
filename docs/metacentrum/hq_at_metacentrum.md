---
title: "Running multi-cluster jobs on MetaCentrum, Phoebe and Koios"
wikijs_updated: 2024-07-26
tags:
  - "hyperqueue"
  - "metacentrum"
---

# Running multi-cluster jobs on MetaCentrum, Phoebe and Koios

!!! tip "Log in without a password"
    Instead of keeping your MetaCentrum password in `~/.bashrc` as shown below, set up
    [passwordless SSH with Kerberos](../systems/metacentrum/kerberos.md) and use
    `ssh metacentrum`.

## Using HyperQueue as a unifying layer on top of multiple clusters


### Tweak your local workstation

Unfortunately, Metacentrum relies on password authentization, so to make our life easier, create alias in your `~/.bashrc` for quick access of `tarkil` - front-end / login node located in Prague.

```
METACENTRUM_PASS=Whatever
METACENTRUM_USER=Eve
METACENTRUM_HOST=tarkil.grid.cesnet.cz

alias go2tarkill="sshpass -p ${METACENTRUM_PASS} ssh ${METACENTRUM_USER}@${METACENTRUM_HOST}"
```

reload shell, or `source ~/.bashrc` in your current shell.

### Configure and run `hq server` on the MetaCentrum oven node
