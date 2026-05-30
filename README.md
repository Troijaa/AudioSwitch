# AudioSwitch

Kleines Tray-Tool für Linux Mint / Cinnamon zum schnellen Wechseln zwischen zwei Audio-Ausgängen.

## Features

- Tray-Icon in der Taskleiste (Lautsprecher oder Headset)
- **Linksklick** → wechselt sofort zwischen den zwei gewählten Ausgängen
- **Rechtsklick** → Menü mit Ausgängen, Einstellungen und Beenden
- **Einstellungen** → beliebige Ausgänge auswählen und Icon zuweisen
- Autostart-fähig

## Voraussetzungen

```bash
sudo apt install python3-gi python3-pil pulseaudio-utils
pip3 install --user --break-system-packages pystray
```

## Starten

```bash
python3 audio_switch.py
```

## Autostart

```bash
cp audio_switch.desktop ~/.config/autostart/
```

## Kompatibilität

- Linux Mint 21+ mit Cinnamon
- PipeWire oder PulseAudio
