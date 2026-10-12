---
title: "Using MetaCentrum with Claude"
description: "Use the metacentrum skill in Claude Code to set up your MetaCentrum account and Kerberos login, write PBS job scripts, submit them and find out why a job failed"
tags:
  - "metacentrum"
  - "ai"
---

# Using MetaCentrum with Claude skill

The **metacentrum skill** teaches [Claude](https://claude.ai), Anthropic's AI assistant, how
to use [MetaCentrum](../systems/metacentrum/index.md), the Czech national grid run by CESNET.
It is the MetaCentrum counterpart of the [ceico-compute skill](claude-skill.md) for Phoebe and
Koios. With it, Claude Code can help you with:

* **your account**: who can register, how to apply, change the password and renew the account
  every year
* **logging in**: choosing a frontend, getting a Kerberos ticket, SSH with Kerberos and fixing
  a login that fails; optionally a ticket obtained at desktop login and renewed automatically,
  as described in [Passwordless SSH with Kerberos](../systems/metacentrum/kerberos.md)
* **storage**: the `/storage/<site>/home` directories, which frontend sees which storage,
  backups and scratch space
* **PBS jobs**: job scripts with `qsub` resources, walltime and scratch staging, the `oven`
  queue for long-running services, [HyperQueue](../systems/metacentrum/hyperqueue.md) for many
  small tasks, following a job and finding out why it failed
* **GPUs**: requesting GPUs, finding which GPU clusters are free *and* open to you (some are
  reachable only through queues restricted to certain groups) and checking the GPU inside a job

Queues, nodes and modules on MetaCentrum change often. The skill treats them as live data and
checks them on a frontend (`qstat`, `pbsnodes`, `module avail`) before it relies on them. Its
source is on GitHub:
[ceico-cz/metacentrum-compute-skill](https://github.com/ceico-cz/metacentrum-compute-skill).

## What you need

* A MetaCentrum account, see [Get an account](../systems/metacentrum/index.md#get-an-account).
  The skill can guide you through the registration, but you fill in the form yourself.
* A seat in one of the CEICO organizations on claude.ai, **CEICO-Cosmo** or **CEICO-FZU**
  (ask the cluster administrator). The metacentrum skill is in the skill library of both.
* [Claude Code](https://code.claude.com/docs) on your computer, signed in with that
  claude.ai account (`claude` in a terminal, or the Code tab of the Claude desktop app).
  Claude needs a shell with `ssh` to reach a MetaCentrum frontend.

In the claude.ai chat, without a terminal, the skill can still answer questions and write job
scripts, but you copy them to the frontend and submit them yourself.

Without a seat in either organization, you can install the skill yourself as a Claude Code
plugin:

```text
/plugin marketplace add ceico-cz/metacentrum-compute-skill
/plugin install metacentrum@ceico-metacentrum
```

or copy the directory `skills/metacentrum` from the
[repository](https://github.com/ceico-cz/metacentrum-compute-skill) into `~/.claude/skills/`.
The same directory works with OpenAI Codex in `~/.codex/skills/`.

## Check that you have the skill

The skill comes with your CEICO-Cosmo or CEICO-FZU seat; you don't install anything. Type
`/skills` in Claude Code to list your skills: **metacentrum** should be among them. If it is
missing, quit Claude Code and start it again so that it loads the organization's skills, and
check that you are signed in with that organization's account.

You don't call the skill by name. Claude uses it whenever you mention MetaCentrum, PBS or
`qsub`.

## Use it

Start Claude Code in the directory with your code and describe what you want, for example:

```text
Set up Kerberos SSH to the MetaCentrum frontend metafzu.fzu.cz for my user novak.
```

```text
Write a PBS script that runs train.py on one GPU with 32 GB RAM for 12 hours, using scratch.
```

```text
Which GPU clusters on MetaCentrum can I actually submit to right now?
```

```text
My job 12345678.pbs-m1.metacentrum.cz finished but produced no output. Find out why.
```

Claude asks only for what it can't find out itself, usually your MetaCentrum username, the
frontend, the command to run and the resources it needs. When it writes a job script, it
explains every placeholder you have to fill in, uses `$SCRATCHDIR` if you asked for scratch and
copies the results back to your home before the job ends. After the job ends, it checks the
exit status, the resources used and the output before it calls the job a success.

Claude Code asks for your permission before it runs commands, unless you have allowed them.
Read what it wants to run, as you would for a colleague typing on your account.

## What the skill does not do

* It never asks for your password, Kerberos ticket cache, private keys or tokens. Run `kinit`
  and type the password yourself.
* On its own, it only looks: it reads queues, nodes and job states. It submits (`qsub`) or
  cancels (`qdel`) jobs and changes your configuration only when you ask.
* It doesn't run computations on a frontend; frontends are for logging in, preparing files
  and PBS commands.
* It can't change your MetaCentrum quotas, group memberships or queue access. For those,
  contact [MetaCentrum user support](https://docs.metacentrum.cz/).

## Good to know

* Everything Claude reads, including your code, job output and file names, is sent to
  Anthropic to be processed. Don't use it with data you are not allowed to share with a cloud
  service.
* Claude can make mistakes. Check the job script it shows you, especially the walltime,
  memory, scratch size and the number of GPUs, before you agree to submit.
* MetaCentrum is a third-party system; its [own documentation](https://docs.metacentrum.cz/)
  is authoritative. If the skill gives outdated information, open an issue in
  [ceico-cz/metacentrum-compute-skill](https://github.com/ceico-cz/metacentrum-compute-skill/issues),
  with usernames and job IDs removed.
