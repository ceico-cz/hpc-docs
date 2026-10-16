#!/usr/bin/env bash
# Installs the Colab SSH Bridge native companion for Firefox, including the
# Ubuntu snap Firefox. Usage: curl -fsSL https://hpc.ceico.cz/compute/colab/install.sh | bash
set -euo pipefail

main() {
  local version=a0c0bd5e34f6 sha256=7cf84d61f9dea1a407ef2ddd916ba0f4fae66b2d52c07479684d54aaedec6855
  local url=https://hpc.ceico.cz/compute/colab/colab-ssh-bridge-companion-$version.tar.gz
  fail() { printf 'error: %s\n' "$1" >&2; exit 1; }

  command -v python3 >/dev/null 2>&1 || fail "python3 is required: sudo apt install python3"
  python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))' ||
    fail "Python 3.11 or later is required; found $(python3 -V 2>&1)"
  command -v ssh >/dev/null 2>&1 || fail "OpenSSH is required: sudo apt install openssh-client"
  command -v curl >/dev/null 2>&1 || fail "curl is required: sudo apt install curl"

  # Global, not local: the EXIT trap runs after main has returned.
  work=$(mktemp -d)
  trap 'rm -rf -- "$work"' EXIT
  curl -fsSL --proto '=https' --max-time 120 -o "$work/companion.tar.gz" -- "$url" ||
    fail "cannot download $url"
  printf '%s  %s\n' "$sha256" "$work/companion.tar.gz" | sha256sum -c --quiet - ||
    fail "the downloaded companion does not match its SHA-256; nothing was installed"
  tar -xzf "$work/companion.tar.gz" -C "$work"
  COLAB_BRIDGE_BUILD=$version "$work/colab-ssh-bridge/scripts/install-native-host.sh"
  printf 'Companion %s installed.\n' "$version"

  if snap list firefox >/dev/null 2>&1; then
    printf '%s\n' "Snap Firefox detected: the first time the extension starts the companion," \
      "Ubuntu asks whether Firefox may launch \"Colab SSH Bridge\". Choose Allow."
  fi
  printf 'Restart Firefox to pick it up.\n'
}

main "$@"
