---
title: "Slurm accounting admin notes"
wikijs_updated: 2025-09-11
description: "experience gained when operating slurm"
tags:
  - "admin"
  - "slurm"
---

# Slurm accounting admin notes

## limit amount of cpus per user

here we create specific qos:

```
sacctmgr create qos max400cpu
sacctmgr modify qos max400cpu set maxtresperuser=cpu=400
sacctmgr modify user name=UserName set defaultqos=max400cpu qos=max400cpu
```

if there are any jobs queued, we need to change qos there too:

```
scontrol update job=123456 qos=max400cpu
```

## Create user in accounting db and associate with account

```
sacctmgr create user name=UserName account=AccountName
```

## Limit amount of actively used gres per user

eg. we want to limit amount of GPU at cluster used by single user:

```
acctmgr modify qos normal set maxtresperuser=gres/gpu:a100=6
```
