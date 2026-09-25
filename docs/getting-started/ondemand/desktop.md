---
title: "Remote desktop in Open OnDemand"
wikijs_updated: 2023-11-15
---

# Remote desktop in Open OnDemand

Open a graphical Linux desktop running on a Phoebe compute node in your browser, for example
to use [Wolfram Mathematica](../../software/mathematica/index.md). First
[log in to Open OnDemand](index.md#log-in).

## Start a desktop session

Click the **Phoebe CPU Desktop** icon.

![Open OnDemand dashboard with the Phoebe CPU Desktop app pinned](screenshot_20220905_190751.png)

In the form, set how many hours the session may run (e.g. 8) and click **Launch**. This submits
the desktop session as a job to Slurm.

![Phoebe CPU Desktop launch form with partition and number of hours](screenshot_20220905_191135.png)

## Wait for the job to start

The session is first shown as **Queued**, with a light blue header.

![Desktop session card in the Queued state](screenshot_20220905_192347.png)

## Open the desktop

When Slurm has found resources, the header turns green and a blue **Launch Phoebe CPU Desktop**
button appears. Set both **Compression** and **Image Quality** to 9 (the highest) for the
sharpest picture, then click the button. The desktop opens in a new browser tab.

![Desktop session card in the Running state with compression and image quality sliders](screenshot_20220905_192559.png)

![Remote Xfce desktop running on a Phoebe compute node](screenshot_20220905_192859.png)

To come back to the session later or end it, see
[reconnect](index.md#reconnect-to-a-running-session) and [end a session](index.md#end-a-session).
