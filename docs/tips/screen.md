---
title: "Screen sessions"
wikijs_updated: 2024-07-19
---

# Screen sessions

GNU `screen` keeps terminal sessions running on the login node after you disconnect, and lets
you open several shells ("windows", shown as tabs below) in one SSH connection. It is how you
keep an [interactive session](../slurm/interactive.md) or a
[VS Code tunnel](../getting-started/vscode-tunnel.md) alive. The login node has screen 4.6.

## Start, leave and come back

| Command | What it does |
| --- | --- |
| `screen -S work` | start a new session named `work` |
| `screen -ls` | list your sessions |
| `screen -r work` | reattach to the session `work` |
| `screen -d -r work` | reattach, detaching it first from wherever else it is still attached |
| `exit` in the last window | end the session |

A detached session keeps running, including everything started in it, until you end it or the
login node restarts.

## Keys inside screen

Every screen command starts with the **prefix key** ++ctrl+a++. The command is two separate key
presses, not one chord: press ++ctrl+a++, **release both keys**, then type the command
character. For example, to open a new window, press ++ctrl+a++, let go, then type `c`.

Command characters are case-sensitive: `a` and `A` do different things.

| Keys | What it does |
| --- | --- |
| ++ctrl+a++ then `d` | detach: leave the session running and return to the login shell |
| ++ctrl+a++ then `c` | create a new window |
| ++ctrl+a++ then `n` / `p` | go to the next / previous window |
| ++ctrl+a++ then `0` … `9` | go to window 0 to 9 |
| ++ctrl+a++ then `"` | list the windows and choose one |
| ++ctrl+a++ then `A` (capital, ++shift+a++) | rename the current window |
| ++ctrl+a++ then `[` | scroll back through the output (move with the arrow keys, leave with ++esc++) |
| ++ctrl+a++ then `k` | close the current window (asks for confirmation) |
| ++ctrl+a++ then `a` | send a literal ++ctrl+a++ to the program, for example to jump to the start of the line in Bash |
| ++ctrl+a++ then `?` | show all key bindings |

The full list is in the GNU Screen manual, under
[default key bindings](https://www.gnu.org/software/screen/manual/html_node/Default-Key-Bindings.html);
see also the [whole manual](https://www.gnu.org/software/screen/manual/screen.html).

## Show windows as tabs

By default screen shows no sign of which windows are open. With this `~/.screenrc` on the login
node, a status line at the bottom lists the windows like tabs, with the host name and the time:

```shell
# Use bash
shell /bin/bash

autodetach on

# Big scrollback
defscrollback 5000

# No annoying startup message
startup_message off

# Display the status line at the bottom
hardstatus on
hardstatus alwayslastline
hardstatus string "%{.kW}%-w%{.bW}%t [%n]%{-}%+w %=%{..G} %H %{..Y} %Y/%m/%d %c"
```

The current window is highlighted in the status line:

![GNU screen status line with open tabs, hostname and time](../screenshots/screenshot_20240115_154445.png)

## tmux

`tmux` (version 2.7) is installed too. It does the same job with a different prefix key
(++ctrl+b++) and commands; see its [getting started guide](https://github.com/tmux/tmux/wiki/Getting-Started).
