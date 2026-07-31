#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# AudioSwitch – Uninstaller
#
# Entfernt AudioSwitch vollständig: Autostart-/Menü-Eintrag, Konfiguration und den
# Installationsordner selbst. Funktioniert aus dem installierten Ort heraus (der
# von install.sh mitkopierte Uninstaller) und entfernt sich dabei selbst.
#
# Systempakete (apt) und pip-Pakete werden bewusst NICHT entfernt, da sie evtl.
# von anderen Programmen genutzt werden.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SELF_DIR="$(dirname "$(readlink -f "$0")")"
INSTALL_DIR="${AUDIOSWITCH_PREFIX:-$HOME/.local/share/AudioSwitch}"

echo "==> Autostart- und Menü-Eintrag entfernen"
rm -f "$HOME/.config/autostart/audioswitch.desktop"
rm -f "$HOME/.local/share/applications/audioswitch.desktop"

echo "==> Konfiguration entfernen (~/.config/audioswitch)"
rm -rf "$HOME/.config/audioswitch"

# Installationsordner entfernen. Wenn dieser Uninstaller aus dem installierten Ort
# läuft, löscht er sich selbst mit – unter Linux unkritisch, da bereits geladen.
TARGET="$INSTALL_DIR"
if [ -d "$SELF_DIR" ] && [ "$SELF_DIR" != "$INSTALL_DIR" ] \
   && [ -f "$SELF_DIR/audio_switch.py" ]; then
    # Uninstaller läuft aus einem anderen (installierten) Ort → diesen entfernen.
    TARGET="$SELF_DIR"
fi

if [ -d "$TARGET" ]; then
    echo "==> Installationsordner entfernen: $TARGET"
    rm -rf "$TARGET"
fi

echo "==> Fertig. AudioSwitch wurde entfernt."
echo "    Hinweis: apt-/pip-Pakete wurden nicht entfernt."
echo "    Bei Bedarf manuell: pip3 uninstall pystray"
