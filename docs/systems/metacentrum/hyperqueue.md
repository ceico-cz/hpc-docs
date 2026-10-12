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

```text
hq worker (PBS job, MetaCentrum)         --+
hq worker (Slurm job, Phoebe)            --+
hq worker (Slurm job, Koios)             --+--> hq server
hq submit, hq job list (any login node)  --+    (PBS job in the oven queue,
                                                 oven.grid.cesnet.cz)
```

Workers and clients connect to the server, never the other way round. The Phoebe and Koios login
and compute nodes can reach the MetaCentrum `oven` node, so no tunnels are needed.

## Before you start

* A [MetaCentrum account](index.md#get-an-account) and an account on
  [Phoebe and Koios](../../getting-started/account.md).
* [Passwordless SSH to MetaCentrum with Kerberos](kerberos.md), so that `ssh metacentrum`
  works without typing a password. Do not store your MetaCentrum password in `~/.bashrc` or
  use `sshpass`.

Throughout this guide, replace `LOGIN` with your MetaCentrum username, and
`/storage/praha1/home/LOGIN` with your home directory on the MetaCentrum frontend (`echo $HOME`
on `metafzu.fzu.cz`).

## 1. Install HyperQueue

HyperQueue is a single static binary. Install the same version on every cluster: on the
MetaCentrum frontend, on the Phoebe login node and on the Koios login node.

```bash
VER=v0.26.2
mkdir -p ~/tools/hq-$VER && cd ~/tools/hq-$VER
curl -sSLO https://github.com/It4innovations/hyperqueue/releases/download/$VER/hq-$VER-linux-x64.tar.gz
tar xzf hq-$VER-linux-x64.tar.gz
./hq --version
```

Check the [releases page](https://github.com/It4innovations/hyperqueue/releases) for the
current version. Clients, server and workers must run the same version.

## 2. Start the server on the oven node

MetaCentrum has a PBS queue called `oven` for long, lightweight jobs: up to 720 hours of
walltime, 1 CPU and 100 MB of memory by default. Its jobs run on `oven.grid.cesnet.cz`. The
`hq server` uses almost no CPU, so it fits there.

On the MetaCentrum frontend, save this as `~/hq/hq-server.pbs`:

```bash
#!/bin/bash
#PBS -N hq-server
#PBS -q oven
#PBS -l select=1:ncpus=1:mem=1gb:scratch_local=1gb
#PBS -l walltime=168:00:00
#PBS -j oe

HQ=/storage/praha1/home/LOGIN/tools/hq-v0.26.2/hq
export HQ_SERVER_DIR=/storage/praha1/home/LOGIN/hq/server

mkdir -p "$HQ_SERVER_DIR"
$HQ server start \
    --host "$(hostname -f)" \
    --client-port 51001 --worker-port 51002 \
    --journal "$HQ_SERVER_DIR/journal.bin"
```

and submit it:

```bash
cd ~/hq && qsub hq-server.pbs
```

!!! warning "Use absolute paths in MetaCentrum job scripts"
    `$HOME` depends on the node a job runs on. On the `oven` node it is
    `/storage/brno2/home/LOGIN`, not the frontend's home directory. With `$HOME/tools/...` the
    server job fails with `No such file or directory`. All `/storage/*` directories are mounted
    on every MetaCentrum node, so absolute paths work everywhere.

The options:

* `--host "$(hostname -f)"` makes the server advertise the full name `oven.grid.cesnet.cz`,
  which workers on Phoebe and Koios can resolve.
* Fixed ports (`51001` for clients, `51002` for workers) make the setup easier to debug than
  random ports. Pick other ports if they are taken.
* `--journal` saves the server state. If the server job ends, submit it again with the same
  journal: unfinished tasks are restored, and workers can reconnect.

When the job is running, check the server from the frontend:

```bash
export HQ_SERVER_DIR=~/hq/server
~/tools/hq-v0.26.2/hq server info
```

The server writes its connection details and keys to `$HQ_SERVER_DIR/hq-current/access.json`.
Every client and worker needs this file.

## 3. Copy the access file to Phoebe and Koios

Copy `access.json` into the same layout on the other clusters, directly from host to host:

```bash
for host in phoebe.fzu.cz koios1.fzu.cz; do
    ssh $host 'mkdir -p ~/hq/server/hq-current && chmod 700 ~/hq/server'
    scp -3 metacentrum:hq/server/hq-current/access.json $host:hq/server/hq-current/access.json
    ssh $host 'chmod 600 ~/hq/server/hq-current/access.json'
done
```

!!! danger "The access file is a password"
    Anyone with `access.json` can run any command as you on every worker. Keep it mode `600`,
    don't put it in a shared or project directory, and don't commit it to git.

A new server (one started without the old journal) gets new keys, so copy the file again after
each new start.

Check that Phoebe can reach the server:

```bash
ssh phoebe.fzu.cz 'HQ_SERVER_DIR=~/hq/server ~/tools/hq-v0.26.2/hq server info'
```

## 4. Start workers

A worker is an ordinary batch job that runs `hq worker start`. It takes tasks from the server
until its walltime runs out, or until it has been idle for `--idle-timeout`.

=== "MetaCentrum (PBS)"

    ```bash
    #!/bin/bash
    #PBS -N hq-worker
    #PBS -l select=1:ncpus=8:mem=16gb:scratch_local=10gb
    #PBS -l walltime=24:00:00
    #PBS -j oe

    HQ=/storage/praha1/home/LOGIN/tools/hq-v0.26.2/hq
    export HQ_SERVER_DIR=/storage/praha1/home/LOGIN/hq/server

    # mem is in MiB and must match the mem= request above (16gb = 16384 MiB)
    $HQ worker start --manager pbs --detect-resources cpus \
        --resource "mem=sum(16384)" --idle-timeout 10m
    ```

    Submit with `qsub hq-worker.pbs`.

=== "Phoebe and Koios (Slurm)"

    ```bash
    #!/bin/bash
    #SBATCH --job-name=hq-worker
    #SBATCH --partition=cpu
    #SBATCH --nodes=1
    #SBATCH --ntasks=1
    #SBATCH --cpus-per-task=8
    #SBATCH --mem=16G
    #SBATCH --time=24:00:00

    export HQ_SERVER_DIR=$HOME/hq/server
    $HOME/tools/hq-v0.26.2/hq worker start --manager slurm --idle-timeout 10m
    ```

    Submit with `sbatch hq-worker.sbatch`.

With `--manager pbs` or `--manager slurm` the worker takes its CPU count and time limit from the
batch job, so tasks are not started if they cannot finish before the job ends.

!!! warning "Limit resource detection on MetaCentrum"
    On MetaCentrum the worker sees the whole node, not just the PBS allocation. In a test, a
    2-CPU, 2 GB job on a GPU node reported 2 GPUs and 1.5 TB of memory that the job had not
    asked for, and HyperQueue would hand out tasks that need them. `--detect-resources cpus`
    detects only the CPUs (which `--manager pbs` limits to the allocation), and
    `--resource "mem=sum(...)"` declares the memory the job really has. If you need GPUs,
    request them with `ngpus=N` in `#PBS -l select=...` and add `--detect-resources cpus,gpus/nvidia`.
    On Phoebe and Koios the defaults are correct, because Slurm confines the job.

List the connected workers from any cluster:

```bash
hq worker list
```

```text
+----+---------+---------------------+----------------------+---------+--------------------------------+
| ID | State   | Hostname            | Resources            | Manager | Manager Job ID                 |
+----+---------+---------------------+----------------------+---------+--------------------------------+
|  1 | RUNNING | n6.phoebe.lan       | cpus 4; mem 4.00 GiB | SLURM   | 3320174                        |
|  2 | RUNNING | eluo1-3.hw.elixir-czech.cz | cpus 2; mem 2.00 GiB | PBS | 24607565.pbs-m1.metacentrum.cz |
|  3 | RUNNING | s1.koios.lan        | cpus 2; mem 2.00 GiB | SLURM   | 3643635                        |
+----+---------+---------------------+----------------------+---------+--------------------------------+
```

## 5. Submit tasks

Set `HQ_SERVER_DIR` in your shell (or in `~/.bashrc` on each cluster) so that `hq` finds the
server:

```bash
export HQ_SERVER_DIR=~/hq/server          # on MetaCentrum
export PATH=~/tools/hq-v0.26.2:$PATH
```

A task can run on any worker, on any cluster. By default HyperQueue runs a task in the
directory it was submitted from and writes its stdout and stderr there. That path exists only
on the cluster you submitted from, so on the other clusters the task fails:

```text
Cannot create stdout directory at File { path: "/auto/vestec1-elixir/home/LOGIN/out/1-1.out", ... }:
Permission denied
```

Make the tasks independent of the submit directory:

```bash
hq submit --name test --array 1-16 --cpus 1 \
    --cwd /tmp --stdout none --stderr none \
    -- bash -c 'out=$HOME/hq-out; mkdir -p $out
                { echo "task $HQ_TASK_ID on $(hostname -f)"; sleep 15; } \
                    > $out/$HQ_JOB_ID-$HQ_TASK_ID.out 2>&1'
```

* `--cwd /tmp` uses a directory that exists everywhere.
* `--stdout none --stderr none` turns off HyperQueue's own output files. The task writes its
  output itself, to a path it builds on the worker.
* The single quotes make `$HOME`, `$HQ_JOB_ID` and `$HQ_TASK_ID` expand on the worker, not at
  submission. `$HOME` is `/home/LOGIN` on Phoebe and Koios, and differs between MetaCentrum
  nodes, but every node can write to it.
* `--array 1-16` creates 16 tasks. Each task gets its index in `$HQ_TASK_ID`.

The same rule applies to input files and programs: either install them under the same path on
every cluster, or let the task copy what it needs (for example with `scp` or `rsync` from a
fixed location) and copy its results back.

## 6. Follow the tasks

```bash
hq job list --all          # all jobs and their state
hq job info 1              # details of job 1
hq task list 1             # every task of job 1, with the worker it ran on
hq task list 1 -v          # the same, with full error messages
```

`hq task list` shows where each task ran:

```text
+---------+----------+---------------------+----------+-------+
| Task ID | State    | Worker              | Makespan | Error |
+---------+----------+---------------------+----------+-------+
|       1 | FINISHED | n6.phoebe.lan       | 15s      |       |
|       2 | FINISHED | alfrid2.meta.zcu.cz | 15s      |       |
|       3 | FINISHED | s1.koios.lan        | 15s      |       |
...
```

Failed tasks can be resubmitted with `hq job resubmit 1 --filter=failed`.

## 7. Stop the workers and the server

Workers stop on their own after `--idle-timeout` with no work, or when their batch job ends.
To stop them earlier:

```bash
hq worker stop all
```

When all your work is done, stop the server, so it doesn't hold an `oven` slot for days:

```bash
hq server stop
```

Delete `~/hq/server/hq-current/access.json` on Phoebe and Koios afterwards, or keep the
directory if you plan to restart the server from its journal.

## Troubleshooting

`Invalid server directory` / `is not a directory`
:   `HQ_SERVER_DIR` is not set, or the server job has not started yet. Check with `qstat -u LOGIN`
    on MetaCentrum.

`Cannot create event log file at .../journal.bin`
:   The directory for the journal must exist before `hq server start`; the job script above
    creates it with `mkdir -p`.

A worker job runs, but the worker is not in `hq worker list`
:   Check the worker job's output file. If the server was restarted without its journal, the
    `access.json` on Phoebe or Koios is out of date: copy it again.

Tasks stay `WAITING`
:   No worker offers the resources the tasks ask for, for example `--cpus 8` while all workers
    have 4 CPUs. Compare `hq job info` with `hq worker list`.
