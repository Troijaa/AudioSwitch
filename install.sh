#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# AudioSwitch – Installer
#
# Installiert AudioSwitch an einen festen Ort (~/.local/share/AudioSwitch), sodass
# der heruntergeladene Ordner anschließend gelöscht werden kann. Legt Autostart-
# und Menü-Eintrag mit dem korrekten Pfad an und kopiert den Uninstaller mit.
# Der Autostart läuft über autostart.sh (robust gegen das Cinnamon-Tray-Timing).
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SRC_DIR="$(dirname "$(readlink -f "$0")")"
INSTALL_DIR="${AUDIOSWITCH_PREFIX:-$HOME/.local/share/AudioSwitch}"

echo "==> Quelle       : $SRC_DIR"
echo "==> Installiere nach: $INSTALL_DIR"

echo "==> Systemabhängigkeiten installieren (benötigt sudo)"
sudo apt install -y python3-gi python3-pil pulseaudio-utils

echo "==> Python-Abhängigkeit (pystray) installieren"
pip3 install --user --break-system-packages pystray

echo "==> Programmdateien kopieren"
mkdir -p "$INSTALL_DIR"
if [ "$SRC_DIR" != "$INSTALL_DIR" ]; then
    cp -f "$SRC_DIR/audio_switch.py" "$SRC_DIR/autostart.sh" "$SRC_DIR/uninstall.sh" "$INSTALL_DIR/"
fi
chmod +x "$INSTALL_DIR/audio_switch.py" "$INSTALL_DIR/autostart.sh" "$INSTALL_DIR/uninstall.sh"

echo "==> Autostart- und Menü-Eintrag anlegen"
mkdir -p "$HOME/.config/autostart" "$HOME/.local/share/applications"

# Autostart: über autostart.sh (wartet auf den Cinnamon-Tray-Host)
cat > "$HOME/.config/autostart/audioswitch.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=AudioSwitch
Comment=Audio-Ausgang umschalten (Tray)
Exec=$INSTALL_DIR/autostart.sh
Icon=audio-card
Terminal=false
Categories=AudioVideo;Audio;
X-GNOME-Autostart-enabled=true
EOF

# Menü-Starter: direkter Start aus dem Anwendungsmenü
cat > "$HOME/.local/share/applications/audioswitch.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=AudioSwitch
Comment=Audio-Ausgang umschalten (Tray)
Exec=python3 $INSTALL_DIR/audio_switch.py
Icon=audio-card
Terminal=false
Categories=AudioVideo;Audio;
EOF

echo
echo "==> Fertig!"
echo "    Installiert in : $INSTALL_DIR"
echo "    Sofort starten : python3 \"$INSTALL_DIR/audio_switch.py\""
echo "    Autostart      : ab dem nächsten Login aktiv"
echo "    Deinstallieren : \"$INSTALL_DIR/uninstall.sh\""
echo
echo "    Der heruntergeladene Ordner wird nicht mehr benötigt und kann gelöscht werden."
