---
title: "Bash tweaks"
wikijs_updated: 2023-11-15
---

# Bash tweaks

Unless noted otherwise, add these snippets to your `~/.bashrc` on the login node. Bash runs
that file whenever you start a new interactive shell; the tilde `~` stands for your home
directory. Run `source ~/.bashrc` to apply changes to the current shell.

## Keep a complete shell history

By default, Bash keeps only the last 500 commands and writes the history file when a shell
exits, so with several open shells (or `screen` tabs) commands get lost. This keeps up to
99 999 commands and appends each one to the history file as soon as you press ++enter++:

```
shopt -s histappend
HISTSIZE=99999
HISTFILESIZE=99999
PROMPT_COMMAND="history -a${PROMPT_COMMAND:+; $PROMPT_COMMAND}"
```

The last line adds `history -a` to `PROMPT_COMMAND` instead of replacing what may already be
there.

## Fancier prompt

This prompt shows your username, the host name and the current directory in different colours:

```
PS1="\[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]\$ "
```

![Coloured bash prompt showing user, host and working directory](../screenshots/koios_prompt.png)

## Slurm shorthands

```
sacct_nice_format="jobid,User,jobname%22,partition,state,NNodes%5,NodeList,Start,End,Elapsed,UserCPU"
showmyjobs()  { sacct --user="$USER" --format="$sacct_nice_format" --starttime="$(date --date='-1 month' +%F)" "$@"; }
showalljobs() { sacct --allusers   --format="$sacct_nice_format" --starttime="$(date --date='-1 month' +%F)" "$@"; }
alias si='sinfo -R -o "%25N %8u %21H %10t %E"'
```

* `showmyjobs`: your jobs from the last month. Extra options are passed on to `sacct`, for
  example `showmyjobs -X` to show one line per job, without its steps.
* `showalljobs`: everyone's jobs from the last month.
* `si`: nodes that are down or drained, with the reason.

They are functions rather than aliases so that "the last month" is computed each time you run
them, not once when the shell starts. See [job history and troubleshooting](../slurm/troubleshooting.md)
for what the columns and job states mean.

## Show the compiler's include directories

Print the directories `gcc` searches for header files (your directory with `.h` files should be
among them):

```
alias showinclude='echo | gcc -E -Wp,-v -'
```

It shows the paths of the `gcc` that is active: the system GCC 8.5, or the one from a loaded
`foss` module (see [software modules](../software/modules.md)).

## Find your public IP address

Print the IP address your computer uses on the internet, for example when you're unsure because
of NAT or a VPN. Run this on your own computer:

```
curl ifconfig.me
```
