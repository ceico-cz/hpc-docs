---
title: "Getting started"
description: "From a new account to your first job on Phoebe and Koios"
---

# Getting started

Phoebe and Koios share user accounts, SSH keys and home directories, so one account works on
both clusters.

!!! warning "Institute network or VPN required"
    Most Phoebe and Koios web services, including the internal Open OnDemand portal, are
    reachable only from FZU networks or over the FZU VPN; from elsewhere they show the page
    "This service is available only from the FZU network". From outside, use the
    [external Open OnDemand portal](ondemand/index.md#two-portals), or the
    [SOCKS proxy over SSH](socks-proxy.md) if you have an FZU account. SSH to the login nodes
    works from anywhere.

## 1. Get an account

1. [Create an SSH key](ssh-key.md) on your laptop or workstation.
2. [Request an account](account.md) and send the administrators your public key.

## 2. Connect

Choose how you want to work:

* [SSH](ssh.md): a terminal on the login node, for everything including batch jobs
* [JupyterLab](ondemand/jupyterlab.md): Python notebooks in your browser, through Open OnDemand
* [Remote desktop](ondemand/desktop.md): a graphical desktop in your browser, for example for
  Mathematica
* [VS Code remote tunnel](vscode-tunnel.md): your local VS Code editing files on the cluster

## 3. Run your first job

The login node is shared by everyone. Run your computations as jobs on the compute nodes:

* [Submit a batch job](../slurm/batch-jobs.md)
* [Start an interactive session](../slurm/interactive.md)

To copy data to and from the cluster, see [mount storage with sshfs](sshfs.md).

See [storage and software](../systems/storage.md) for where your files live.
