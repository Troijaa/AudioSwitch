# Changelog

Alle nennenswerten Änderungen an AudioSwitch werden in dieser Datei dokumentiert.

Das Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
und das Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [1.1.0] - 2026-07-31

### Hinzugefügt
- Installationsskript `install.sh`: installiert nach `~/.local/share/AudioSwitch`,
  richtet Autostart- und Menü-Eintrag mit korrektem Pfad ein; der heruntergeladene
  Ordner kann danach gelöscht werden.
- Deinstallationsskript `uninstall.sh`: entfernt Starter, Konfiguration
  (`~/.config/audioswitch`) und den Installationsordner vollständig.
- Robuster Login-Start über `autostart.sh` (wartet auf den Cinnamon-Tray-Host,
  behebt den Absturz/SIGTRAP beim Anmelden).
- Single-Instance-Schutz per Datei-Lock: eine zweite Instanz beendet sich sauber.
- Versionsanzeige im Tray-Menü sowie `--version` / `-V` auf der Kommandozeile.

### Geändert
- README mit skriptbasierter Installation und Deinstallation aktualisiert.
- `audio_switch.desktop` zu einer neutralen Vorlage gemacht (vorher hartkodierter,
  fremder Pfad).

### Behoben
- `install.sh` brach ab, wenn `pip3` nicht vorhanden war. Die unnötige
  `pystray`-Abhängigkeit (wird vom Programm nicht verwendet) wurde entfernt; das
  Tray-Icon läuft über `XApp.StatusIcon`. Zusätzlich wird `gir1.2-xapp-1.0` als
  Abhängigkeit installiert.

## [1.0.0] - 2026-05-30

### Hinzugefügt
- Erste Version: Audio-Ausgabe-Umschalter für Linux mit System-Tray-Icon.
- Linksklick wechselt zwischen zwei gewählten Ausgängen.
- Rechtsklick-Menü mit Ausgängen, Einstellungen und Beenden.
- Einstellungen zum Auswählen der Ausgänge und Zuweisen von Icons.
- Autostart-Unterstützung.

[1.1.0]: https://github.com/Troijaa/AudioSwitch/releases/tag/v1.1.0
[1.0.0]: https://github.com/Troijaa/AudioSwitch/releases/tag/v1.0.0
