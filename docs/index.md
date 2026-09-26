---
wikijs_updated: 2024-01-22
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# CEICO HPC Services

High-performance computing for members of the [CEICO project](https://ceico.cz/) at the Institute of Physics (FZU)
of the Czech Academy of Sciences.

[Get started](getting-started/index.md){ .md-button .md-button--primary }
[Log in to Open OnDemand](https://ood.phoebe.ceico.cz){ .md-button }

Web portals need the FZU network or VPN. From elsewhere, use the
[external portal](getting-started/ondemand/index.md#two-portals) or the
[SOCKS proxy](getting-started/socks-proxy.md).

</div>

## Our systems

<div class="grid cards" markdown>

-   :material-server-network:{ .lg } **Phoebe**

    ---

    The current CEICO cluster: 1408 CPU cores and 16 NVIDIA A100 GPUs on 100 Gb/s InfiniBand.

    [:octicons-arrow-right-24: About Phoebe](systems/phoebe/index.md)

-   :material-server:{ .lg } **Koios**

    ---

    The previous-generation CEICO cluster: 864 CPU cores, sharing accounts with Phoebe.

    [:octicons-arrow-right-24: About Koios](systems/koios/index.md)

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

    [:octicons-arrow-right-24: Account setup](getting-started/account.md)

-   :material-console:{ .lg } **Command line (SSH)**

    ---

    Log in to `phoebe.fzu.cz` or `koios1.fzu.cz` from Linux, macOS or Windows.

    [:octicons-arrow-right-24: Connect with SSH](getting-started/ssh.md)

-   :material-language-python:{ .lg } **JupyterLab in the browser**

    ---

    Run Python notebooks on Phoebe through the Open OnDemand portal.

    [:octicons-arrow-right-24: Start JupyterLab](getting-started/ondemand/jupyterlab.md)

-   :material-monitor:{ .lg } **Remote desktop**

    ---

    Use graphical applications such as Wolfram Mathematica in a desktop session.

    [:octicons-arrow-right-24: Open a desktop](getting-started/ondemand/desktop.md)

</div>

## Run your work

<div class="grid cards" markdown>

-   [:material-tray-arrow-up: **Submit a batch job**](slurm/batch-jobs.md)

    Write a Slurm job script and queue it.

-   [:material-expansion-card: **GPU jobs**](slurm/gpu-jobs.md)

    Request NVIDIA A100 GPUs on Phoebe.

-   [:material-timer-play-outline: **Interactive session**](slurm/interactive.md)

    Get a shell on a compute node for testing and debugging.

-   [:material-bug-outline: **Troubleshoot a job**](slurm/troubleshooting.md)

    Find out why a job failed or is still waiting.

</div>

## Help and more

<div class="grid cards" markdown>

-   [:material-lifebuoy: **Get help**](getting-started/account.md)

    Contact the CEICO HPC administrator.

-   [:material-package-variant: **Software**](software/index.md)

    Software modules, conda, uv and guides for specific applications.

-   [:material-folder-outline: **Storage**](systems/storage.md)

    Where your files live: home directories, project space and local scratch.

-   [:material-format-quote-close: **Acknowledge Phoebe**](systems/phoebe/acknowledgement.md)

    Text to include in your publications.

</div>

!!! warning "TODO"
    - Give "Get help" a real support contact (e-mail address, Slack or ticket system); it
      currently points to the account page.
    - Add where planned maintenance is announced (mailing list, Slack channel or status page).
    - Use one full name for CEICO: the footer says "Central European Institute for Cosmology and
      Fundamental Physics", the acknowledgement template "Central European Institute of
      Cosmology".
