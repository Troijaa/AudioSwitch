#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# AudioSwitch – robuster Login-Start
#
# Problem: Beim Login startet audio_switch.py oft, BEVOR der Cinnamon-System-Tray
# (XApp StatusIcon-Host) auf DBus bereit ist. XApp.StatusIcon findet dann keinen
# Host -> Absturz (SIGTRAP). Eine feste Wartezeit (sleep 5) ist unzuverlässig.
#
# Lösung: Aktiv warten, bis der Tray-Host "org.x.StatusIconMonitor.cinnamon"
# auf dem Session-DBus erscheint – dann erst starten. Mit Timeout-Fallback.
# ─────────────────────────────────────────────────────────────────────────────

DIR="$(dirname "$(readlink -f "$0")")"
export DISPLAY="${DISPLAY:-:0}"

# Bis zu 60 Sekunden auf den Cinnamon-Tray-Host warten
for _ in $(seq 1 60); do
    if dbus-send --session --dest=org.freedesktop.DBus \
            --type=method_call --print-reply /org/freedesktop/DBus \
            org.freedesktop.DBus.ListNames 2>/dev/null \
            | grep -q "org.x.StatusIconMonitor.cinnamon"; then
        break
    fi
    sleep 1
done

# Kleine Sicherheitsmarge, dann starten (exec = ersetzt die Shell)
sleep 1
exec python3 "$DIR/audio_switch.py"
