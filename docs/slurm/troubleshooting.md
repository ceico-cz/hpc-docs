---
title: "Job history and troubleshooting"
wikijs_updated: 2023-11-16
description: "Find past jobs with sacct, understand job states, and see why a job is pending or failed"
---

# Job history and troubleshooting

## Find your jobs with `sacct`

`squeue` shows only queued and running jobs. `sacct` reads the accounting database, so it also
shows jobs that have finished. This command lists your jobs from the past month:

```
sacct --user=$USER --format=jobid,user,jobname%22,partition,state%20,NodeList,Start,End,Elapsed --starttime=$(date --date='-1 month' +%Y-%m-%d)
```

The `%` sets a column width: `jobname%22` reserves 22 characters, so long names are not cut.
Without `--starttime`, `sacct` shows only jobs since midnight.

### Example

Here the job `1410269` was cancelled:

```
$ sacct
JobID           JobName  Partition    Account  AllocCPUS      State ExitCode 
------------ ---------- ---------- ---------- ---------- ---------- -------- 
1410269      sys/dashb+    cpu_int   fzu_a_39         16 CANCELLED+      0:0 
1410269.bat+      batch              fzu_a_39         16  CANCELLED     0:15 
1410269.ext+     extern              fzu_a_39         16  COMPLETED      0:0 
$ 
```

Each job has several lines: the job itself, then its steps (`batch` is the job script,
`extern` is Slurm's own bookkeeping). The first line holds the job's overall state.

## Understand the job state

| State | Meaning | What to do |
| --- | --- | --- |
| `COMPLETED` | The job ended with exit code 0. | - |
| `FAILED` | The job ended with a non-zero exit code, for example after an error or a segmentation fault. | Read the job's [output file](#read-the-jobs-output). |
| `OUT_OF_MEMORY` | The job used more memory than it had. The default is a fixed amount [per CPU](index.md#memory-per-cpu). | Ask for more with `--mem` or `--mem-per-cpu`. |
| `TIMEOUT` | The job reached its `--time` limit and was stopped. | Ask for more time, or make the job save checkpoints. |
| `CANCELLED by <uid>` | Someone cancelled the job with `scancel`. `id -u` shows your own uid. | - |
| `PREEMPTED` | The job ran in the `preempt` partition and was stopped for a higher-ranked job; see [preemption](index.md#preemption-when-a-job-can-be-paused-or-stopped). | It is put back in the queue automatically. |
| `NODE_FAIL` | The node running the job failed. | Resubmit the job. If it happens again, tell the administrators. |
| `SUSPENDED` | The job is paused while a higher-ranked job uses its node. | Nothing; it continues afterwards. |
| `PENDING` | The job is waiting in the queue. | See [why is my job pending?](#why-is-my-job-pending) |
| `RUNNING` | The job is running. | - |

## Why is my job pending?

`squeue --me` shows the reason in the last column, `NODELIST(REASON)`:

```
$ squeue --me
  JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
  10812       gpu   gpu-test   jose PD       0:00      1 (Resources)
```

| Reason | Meaning |
| --- | --- |
| `Resources` | The job is next in line and waits for nodes to become free. |
| `Priority` | Jobs with higher priority are ahead of yours. Your [fair share](index.md#priority-and-fair-share) sets your priority. |
| `QOSMaxGRESPerUser`, `QOSMaxCpuPerUserLimit`, `QOSMaxJobsPerUserLimit` | You have reached a [per-user limit](index.md#per-user-limits). The job starts when some of your other jobs finish. |
| `AssocGrpGRES`, `AssocGrpCpuLimit` | Your account or project has reached its limit. |
| `ReqNodeNotAvail, Reserved for maintenance` | Planned maintenance is coming. The job would not finish before it starts, so it waits. A shorter `--time` may let it run before the maintenance. |

`scontrol show job <jobid>` shows the full details, including `StartTime`: Slurm's estimate of
when a pending job will start.

## Read the job's output

What your job prints goes to a file. By default, both standard output (`stdout`) and error
messages (`stderr`) go to `slurm-<jobid>.out` in the directory you submitted the job from.
`scontrol show job <jobid>` shows the paths as `StdOut` and `StdErr` while the job is known to
Slurm.

To name the files yourself or keep errors separate, add to your job script:

```shell
#SBATCH --output=%x-%j.out   # %x = job name, %j = job ID
#SBATCH --error=%x-%j.err
```

The last lines of the output file usually show why a job failed:

```
tail -n 50 slurm-10811.out
```
