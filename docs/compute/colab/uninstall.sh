#!/usr/bin/env bash
set -euo pipefail

install_dir=${XDG_DATA_HOME:-"$HOME/.local/share"}/colab-ssh-bridge
manifest="$HOME/.mozilla/native-messaging-hosts/cz.ceico.colab_ssh_bridge.json"

if [[ -f "$manifest" ]]; then
  mv -- "$manifest" "$manifest.uninstalled"
  printf 'Disabled native host manifest; recoverable at %s.uninstalled\n' "$manifest"
fi
if [[ -d "$install_dir" ]]; then
  stamp=$(date +%Y%m%d-%H%M%S)
  mv -- "$install_dir" "$install_dir.uninstalled-$stamp"
  printf 'Moved native host files to %s.uninstalled-%s\n' "$install_dir" "$stamp"
fi
config_dir=${XDG_CONFIG_HOME:-"$HOME/.config"}/colab-ssh-bridge
printf 'Profile configuration was preserved under %s\n' "$config_dir"
