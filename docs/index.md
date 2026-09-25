---
wikijs_updated: 2024-01-22
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# CEICO HPC Services

High-performance computing for members of the CEICO project at the Institute of Physics (FZU) of
the Czech Academy of Sciences. This site explains how to get an account, connect to our
clusters and third-party systems, and run your work.

[Get an account](getting-there/getting-a-user-account.md){ .md-button .md-button--primary }
[Browse systems](systems/index.md){ .md-button }

</div>

## Our systems

<div class="grid cards" markdown>

-   :material-server-network:{ .lg } **Phoebe**

    ---

    The current CEICO cluster: 1408 CPU cores and 16 NVIDIA A100 GPUs on 100 Gb/s InfiniBand.

    [:octicons-arrow-right-24: About Phoebe](systems/phoebe.md)

-   :material-server:{ .lg } **Koios**

    ---

    The previous-generation CEICO cluster, sharing accounts and home directories with Phoebe.

    [:octicons-arrow-right-24: About Koios](koios.md)

-   :material-earth:{ .lg } **Third-party systems**

    ---

    External infrastructures available to CEICO members, such as MetaCentrum.

    [:octicons-arrow-right-24: MetaCentrum](systems/metacentrum/index.md)

</div>

## Start working

<div class="grid cards" markdown>

-   :material-account-plus:{ .lg } **Get an account**

    ---

    Create an SSH key pair, then contact the CEICO HPC administrator to set up your account.

    [:octicons-arrow-right-24: Account setup](getting-there/getting-a-user-account.md)

-   :material-console:{ .lg } **Command line (SSH)**

    ---

    Log in to `phoebe.fzu.cz` or `koios1.fzu.cz` from Linux, macOS or Windows.

    [:octicons-arrow-right-24: Connect with SSH](getting-there/ssh.md)

-   :material-language-python:{ .lg } **JupyterLab in the browser**

    ---

    Run Python notebooks on Phoebe through the Open OnDemand portal.

    [:octicons-arrow-right-24: Start JupyterLab](getting-there/using-jupyterLab-at-ondemand.md)

-   :material-monitor:{ .lg } **Remote desktop**

    ---

    Use graphical applications such as Wolfram Mathematica in a desktop session.

    [:octicons-arrow-right-24: Open a desktop](getting-there/desktop.md)

</div>

!!! warning "Network access"
    Most Phoebe and Koios services are available only from Institute networks or over VPN.

## Run your work

<div class="grid cards" markdown>

-   [:material-tray-arrow-up: **Submit a batch job**](submit-job.md)

    Write a Slurm job script and queue it.

-   [:material-timer-play-outline: **Interactive session**](slurm/interactive_slurm_cli_session.md)

    Get a shell on a compute node for testing and debugging.

-   [:material-bug-outline: **Troubleshoot a job**](slurm/slurm_jobs_troubleshooting.md)

    Find out why a job failed or is still waiting.

-   [:material-package-variant: **Software modules**](useful/module_use.md)

    Load compilers, libraries and applications with Lmod.

</div>
