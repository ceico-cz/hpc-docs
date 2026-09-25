---
title: "JupyterLab in Open OnDemand"
wikijs_updated: 2024-09-11
---

# JupyterLab in Open OnDemand

Run Python notebooks on a Phoebe compute node from your browser. First
[log in to Open OnDemand](index.md#log-in).

## How Python is provided

Python itself comes from [Lmod modules](../../software/modules.md). The packages you need are
installed in your own Python virtual environment (venv), which also contains JupyterLab. The
portal creates it for you in `~/.venvs/`.

## Start a session

On the portal, select **VENV-based JupyterLab** and fill in the form:

* **Slurm partition**: `cpu`, or `gpu` if you need GPU acceleration, or `small` for light work.
  The session runs in the matching interactive partition: `cpu_int`, `gpu_int` or `small_int`.
* **Preloaded moduleset**: keep empty.
* **Python version**: the version you need, typically the latest.
* **Session duration**: how long the session may run, from 8 hours to 14 days.
* **Instance size**: the number of CPU cores, from 8 to 128.
* **GPU count**: leave at 0 unless you need GPUs (up to 4).
* **Venv name to be created in ~/.venvs/**: a name for your new virtual environment (default
  `venv_default`).
* **Existing venv path to use**: keep empty; this option is not ready yet.

Click **Launch** to submit the session as a job to Slurm.

## Wait for the job to start

The session is first shown as **Queued**. The first start takes longer, because the portal
creates your virtual environment.

![Jupyter session card in the Queued state](screenshot_20220906_141417.png)

## Connect to the session

Once the session is **Running**, click **Connect to Jupyter**. JupyterLab opens in a new browser
tab.

![Jupyter session card in the Running state with the Connect to Jupyter button](screenshot_20220906_141524.png)

To come back to the session later or end it, see
[reconnect](index.md#reconnect-to-a-running-session) and [end a session](index.md#end-a-session).
