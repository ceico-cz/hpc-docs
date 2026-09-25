---
title: "Multi-cluster jobs with HyperQueue"
wikijs_updated: 2024-07-26
description: "Run one set of tasks across MetaCentrum, Phoebe and Koios with HyperQueue"
---

# Multi-cluster jobs with HyperQueue

[HyperQueue](https://it4innovations.github.io/hyperqueue/stable/) is a task scheduler that runs
on top of existing batch systems. One `hq server` hands out tasks to workers, and the workers can
run as jobs on different clusters: MetaCentrum (PBS Pro), Phoebe and Koios (Slurm). That way one
set of tasks can use all three clusters.

## Before you start

* A [MetaCentrum account](index.md#get-an-account) and an account on
  [Phoebe and Koios](../../getting-started/account.md).
* [Passwordless SSH to MetaCentrum with Kerberos](kerberos.md), so that `ssh metacentrum`
  works without typing a password. Do not store your MetaCentrum password in `~/.bashrc` or
  use `sshpass`.

!!! warning "TODO"
    This guide is not written yet. The original page stopped at its first step,
    "Configure and run `hq server` on the MetaCentrum oven node". Planned sections:

    1. Start `hq server` on a MetaCentrum node that stays up (the "oven" node), and how the
       other clusters reach it.
    2. Start HyperQueue workers as PBS jobs on MetaCentrum and as Slurm jobs on Phoebe and Koios.
    3. Submit tasks with `hq submit` and follow them with `hq job list`.
    4. Stop the workers and the server when done.
