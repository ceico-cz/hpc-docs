---
title: "Running jobs with Claude"
description: "Use the Phoebe skill in Claude Code to check your access, write Slurm job scripts, submit them and follow your jobs"
tags:
  - "slurm"
  - "ai"
---

# Running jobs with Claude

The **Phoebe skill** teaches [Claude](https://claude.ai), Anthropic's AI assistant, how to
use Phoebe. With it, Claude Code can take your code from your laptop to a finished Slurm job:

* check that you can log in to Phoebe, and tell you how to fix it if you can't
* pick a partition and the software: [modules](../software/modules.md),
  [EESSI](../software/eessi.md) on the GPU nodes, [conda](../software/conda.md),
  [uv](../software/python-uv.md) or Apptainer containers
* copy your code to Phoebe, write a job script, show it to you and submit it once you agree
* follow the job, explain why it failed or is still waiting, and copy the results back

The skill knows the partitions, limits, storage and software described on these pages, and
checks the current state on the cluster itself (`sinfo`, `module spider`) before it relies
on anything.

## What you need

* A Phoebe account with your SSH key, see [Get an account](../getting-started/account.md) and
  [SSH key](../getting-started/ssh-key.md). The skill does not create accounts.
* A seat in the **CEICO-Cosmo** organization on claude.ai (ask the cluster administrator).
  The Phoebe skill is in the organization's skill library.
* [Claude Code](https://code.claude.com/docs) on your computer, signed in with that
  claude.ai account (`claude` in a terminal, or the Code tab of the Claude desktop app).
  Claude needs a shell with `ssh` to reach Phoebe.

In the claude.ai chat, without a terminal, the skill can still answer questions and write job
scripts, but you copy them to Phoebe and submit them yourself.

## Turn the skill on

Skills from the organization library appear in claude.ai under **Settings → Capabilities →
Skills**. Make sure **phoebe** is switched on there. Claude Code signed in with the same
account loads it on its next start; type `/skills` in Claude Code to check that `phoebe` is
listed.

You don't call the skill by name. Claude uses it whenever you mention Phoebe.

## Use it

Start Claude Code in the directory with your code and describe what you want, for example:

```text
Run sim.py on Phoebe with 16 cores and 32 GB of memory, it takes about 3 hours.
```

```text
Train train.py on one A100 GPU on Phoebe. My Phoebe username is novak.
```

```text
Why is my Phoebe job 3320029 still pending?
```

Claude then works through these steps:

1. **Checks your login.** It runs a short non-interactive `ssh` test to `phoebe.fzu.cz` and
   compares the server's host key with the [published fingerprint](../getting-started/ssh.md).
   If the login fails, it says why (no key, wrong username, key not registered, network) and
   what to do. Tell it your Phoebe username if it differs from your local one.
2. **Asks what it can't infer** from your code: run time, memory, number of cores or GPUs.
3. **Copies the code** with `rsync` to a directory `~/jobs/<name>/` in your Phoebe home.
4. **Writes the job script** with an explicit time limit, memory, partition and software
   versions, and shows it to you. It submits with `sbatch` only after you agree, or right
   away if you already asked it to run the job.
5. **Follows the job** with `squeue` and `sacct`, reads the output, and checks the efficiency
   with `seff` when the job ends. Results stay on Phoebe unless you ask to copy them back.

Claude Code asks for your permission before it runs commands, unless you have allowed them.
Read what it wants to run, as you would for a colleague typing on your account.

## What the skill does not do

* It doesn't ask for or handle passwords, passphrases or private keys. If your key has a
  passphrase, load it into your SSH agent yourself (`ssh-add`).
* It cancels jobs (`scancel`) and deletes files only when you ask.
* It doesn't run heavy computations on the front-end node; tests and builds that take longer
  than a few minutes go to a compute node.
* It can't change limits, partitions or software installations. For those, contact the
  cluster administrator.

## Good to know

* Everything Claude reads, including your code, job output and file names, is sent to
  Anthropic to be processed. Don't use it with data you are not allowed to share with a cloud
  service.
* Claude can make mistakes. Check the job script it shows you, especially the time limit,
  memory and the number of GPUs, before you agree to submit.
* For long jobs, Claude doesn't need to stay open. Ask it later "how did my Phoebe job
  `<id>` finish?" and it reads the state and output again.
* If the skill gives outdated information about Phoebe, tell the cluster administrator so it
  can be fixed.
