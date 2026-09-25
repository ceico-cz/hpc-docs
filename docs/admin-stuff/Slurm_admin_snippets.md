---
title: "Slurm admin snippets"
wikijs_updated: 2024-06-11
description: "snippets from daily slurm driving"
tags:
  - "admin"
  - "slurm"
---

# Slurm admin snippets

## Resume all jobs on a node

= reactivate suspended jobs at given node, possible to combine with `--user` indeed.

```
for job in $(squeue --noheader -w n14 | awk '{print $1}'| xargs); do scontrol resume job=$job ;done
```

## Create a maintenance reservation

(Phoebe)

```
 scontrol create reservation starttime=2024-06-14T18:00:00 duration=3-00:00:00 flags=MAINT,IGNORE_JOBS Nodes=n[1-20],gpu[1-2],s[1,2] user=root
```

(Koios)

```
scontrol create reservation starttime=2024-06-14T18:00:00 duration=3-00:00:00 flags=MAINT,IGNORE_JOBS Nodes=n[1-27] user=root
```
