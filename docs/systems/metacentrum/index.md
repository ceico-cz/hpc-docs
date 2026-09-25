---
title: "MetaCentrum"
description: "Using the Czech national grid MetaCentrum from CEICO"
---

# MetaCentrum

[MetaCentrum](https://www.metacentrum.cz/en/) is the national grid computing infrastructure
of the Czech Republic, operated by CESNET as part of e-INFRA CZ. It is free for researchers
at Czech academic institutions, including CEICO members, and provides many thousands of CPU
cores and GPUs spread over clusters across the country.

MetaCentrum is a **third-party system**: it has its own accounts, rules, support and
[user documentation](https://docs.metacentrum.cz/). This section covers only what is specific
to CEICO users.

## How it differs from Phoebe and Koios

| | Phoebe and Koios | MetaCentrum |
| --- | --- | --- |
| Account | CEICO account, SSH key | separate MetaCentrum account and password |
| Authentication | SSH key | password or Kerberos ticket (realm `META`) |
| Workload manager | Slurm (`sbatch`, `squeue`) | PBS Pro (`qsub`, `qstat`) |
| Storage | shared BeeGFS home directories | separate storage per site, under `/storage/<site>/` |

## Get an account

Registration needs a valid academic affiliation, which FZU provides. Fill in the short form
linked from the [MetaCentrum account page](https://docs.metacentrum.cz/en/docs/access/account);
new applications are approved manually within a few working days. Accounts expire every year
on 2 February. MetaCentrum emails a renewal request around the turn of the year.

## Log in

The FZU frontend is **`metafzu.fzu.cz`** (also reachable as `metafzu.metacentrum.cz`). It runs
Debian 12 and is dedicated to FZU users; any other
[MetaCentrum frontend](https://docs.metacentrum.cz/en/docs/computing/infrastructure/frontends)
works as well.

```bash
ssh LOGIN@metafzu.fzu.cz
```

This asks for your MetaCentrum password every time. To log in without a password and have
`qsub`, `qstat` and storage access work on the frontend straight away, set up
[passwordless SSH with Kerberos](kerberos.md).

## Guides

<div class="grid cards" markdown>

-   [:material-key-chain: **Passwordless SSH with Kerberos**](kerberos.md)

    Get a Kerberos ticket at desktop login, keep it renewed and use it for SSH.

-   [:material-lan: **Multi-cluster jobs with HyperQueue**](hyperqueue.md)

    Run one set of tasks across MetaCentrum, Phoebe and Koios.

</div>

!!! info "Support"
    For MetaCentrum accounts, quotas and outages, contact
    [MetaCentrum user support](https://docs.metacentrum.cz/), not the CEICO HPC administrator.
