---
title: "Configuring screen for a tabbed view"
wikijs_updated: 2024-07-19
---

# Configuring screen for a tabbed view

## Configuring screen

Into `~/.screenrc` insert:

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

In resulting look, you can see the status line containing open tabs, hostname and current time.

![GNU screen status line with open tabs, hostname and time](../screenshots/screenshot_20240115_154445.png)
