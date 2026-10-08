---
title: "Vim: copy and paste with the mouse"
---

# Vim: copy and paste with the mouse

When Vim has mouse support switched on, selecting text with the mouse starts Vim's own
visual mode instead of selecting text in your terminal, so you cannot copy it to your
computer's clipboard. Pasting with the mouse can also mangle indentation. Many Linux
distributions switch the mouse on by default (Vim's `defaults.vim` sets `mouse=a`), and so
do many `~/.vimrc` files copied from elsewhere.

To see whether this affects you, type `:set mouse?` in Vim. An empty value (`mouse=`) means
the mouse is off and selecting works as in any other terminal program.

## Hold Shift while selecting

The quickest workaround needs no configuration: hold ++shift++ while you select or paste
with the mouse, and the terminal handles the mouse itself. This works in most terminals on
Linux and Windows (GNOME Terminal, Konsole, xterm, Windows Terminal, PuTTY). On macOS, hold
++option++ in iTerm2 or ++fn++ in Terminal.

## Switch the mouse off

For the current Vim session, type:

```
:set mouse=
```

To make it permanent, add the line `set mouse=` to `~/.vimrc`. If you do not have a
`~/.vimrc` yet, create it with this content:

```
unlet! skip_defaults_vim
source $VIMRUNTIME/defaults.vim
set mouse=
```

The first two lines keep Vim's usual defaults (syntax highlighting and similar): Vim loads
them only when no `~/.vimrc` exists, so a `~/.vimrc` containing just `set mouse=` would
turn them off too.
