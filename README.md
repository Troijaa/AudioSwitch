# AudioSwitch

Kleines Tray-Tool für Linux Mint / Cinnamon zum schnellen Wechseln zwischen zwei Audio-Ausgängen.

## Features

- Tray-Icon in der Taskleiste (Lautsprecher oder Headset)
- **Linksklick** → wechselt sofort zwischen den zwei gewählten Ausgängen
- **Rechtsklick** → Menü mit Ausgängen, Einstellungen und Beenden
- **Einstellungen** → beliebige Ausgänge auswählen und Icon zuweisen
- Autostart-fähig

## Installation (empfohlen)

Das Installationsskript richtet alles automatisch ein (Abhängigkeiten, Autostart
und Menü-Eintrag mit dem korrekten Pfad):

```bash
git clone https://github.com/Troijaa/AudioSwitch.git
cd AudioSwitch
./install.sh
```

Entfernen (Autostart- und Menü-Eintrag):

```bash
./uninstall.sh
```

## Manuelle Installation

Voraussetzungen:

```bash
sudo apt install python3-gi python3-pil pulseaudio-utils
pip3 install --user --break-system-packages pystray
```

Starten:

```bash
python3 audio_switch.py
```

Autostart einrichten (robust über `autostart.sh`, das auf den Cinnamon-Tray wartet):

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/audioswitch.desktop <<EOF
[Desktop Entry]
Type=Application
Name=AudioSwitch
Comment=Audio-Ausgang umschalten (Tray)
Exec=$(pwd)/autostart.sh
Icon=audio-card
Terminal=false
Categories=AudioVideo;Audio;
X-GNOME-Autostart-enabled=true
EOF
```

## Kompatibilität

- Linux Mint 21+ mit Cinnamon
- PipeWire oder PulseAudio
