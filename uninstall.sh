#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# AudioSwitch – Uninstaller
#
# Entfernt die von install.sh angelegten Autostart- und Menü-Einträge.
# Systempakete (apt) und pip-Pakete werden bewusst NICHT entfernt, da sie evtl.
# von anderen Programmen genutzt werden. Das Repo-Verzeichnis selbst bleibt.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

echo "==> Autostart- und Menü-Eintrag entfernen"
rm -f "$HOME/.config/autostart/audioswitch.desktop"
rm -f "$HOME/.local/share/applications/audioswitch.desktop"

echo "==> Fertig. AudioSwitch startet nicht mehr automatisch."
echo "    Hinweis: apt-/pip-Pakete wurden nicht entfernt."
echo "    Bei Bedarf manuell: pip3 uninstall pystray"
