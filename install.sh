#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# AudioSwitch – Installer
#
# Richtet AudioSwitch portabel ein: installiert Abhängigkeiten, macht die Skripte
# ausführbar und legt Autostart- sowie Menü-Eintrag mit dem KORREKTEN Pfad an
# (kein hartkodierter Pfad). Der Autostart läuft über autostart.sh, damit der
# Login-Start robust gegen das DBus-Timing des Cinnamon-Trays ist.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

REPO_DIR="$(dirname "$(readlink -f "$0")")"

echo "==> AudioSwitch wird aus: $REPO_DIR installiert"

echo "==> Systemabhängigkeiten installieren (benötigt sudo)"
sudo apt install -y python3-gi python3-pil pulseaudio-utils

echo "==> Python-Abhängigkeit (pystray) installieren"
pip3 install --user --break-system-packages pystray

echo "==> Skripte ausführbar machen"
chmod +x "$REPO_DIR/audio_switch.py" "$REPO_DIR/autostart.sh"

echo "==> Autostart- und Menü-Eintrag anlegen"
mkdir -p "$HOME/.config/autostart" "$HOME/.local/share/applications"

# Autostart: über autostart.sh (wartet auf den Cinnamon-Tray-Host)
cat > "$HOME/.config/autostart/audioswitch.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=AudioSwitch
Comment=Audio-Ausgang umschalten (Tray)
Exec=$REPO_DIR/autostart.sh
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
Exec=python3 $REPO_DIR/audio_switch.py
Icon=audio-card
Terminal=false
Categories=AudioVideo;Audio;
EOF

echo
echo "==> Fertig!"
echo "    Sofort starten : python3 \"$REPO_DIR/audio_switch.py\""
echo "    Autostart      : ist ab dem nächsten Login aktiv"
echo "    Deinstallieren : \"$REPO_DIR/uninstall.sh\""
