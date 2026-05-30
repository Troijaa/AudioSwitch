#!/usr/bin/env python3
import subprocess
import os
import json
import re
import gi
gi.require_version("Gtk", "3.0")
gi.require_version("XApp", "1.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, XApp
from PIL import Image, ImageDraw

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.expanduser("~/.config/audioswitch/config.json")

ICON_TYPES  = ["speaker", "headset"]
ICON_LABELS = {"speaker": "Lautsprecher", "headset": "Headset"}


# ── Icons zeichnen ────────────────────────────────────────────────────────────

def _draw_speaker(d, s, W):
    d.rectangle([int(s*.18), int(s*.38), int(s*.34), int(s*.62)], fill=W)
    d.polygon([
        (int(s*.34), int(s*.38)),
        (int(s*.34), int(s*.62)),
        (int(s*.54), int(s*.76)),
        (int(s*.54), int(s*.24)),
    ], fill=W)
    lw = max(2, int(s*.05))
    d.arc([int(s*.56), int(s*.30), int(s*.72), int(s*.70)], -65, 65, fill=W, width=lw)
    d.arc([int(s*.62), int(s*.22), int(s*.82), int(s*.78)], -65, 65, fill=W, width=lw)


def _draw_headset(d, s, W):
    lw = max(4, int(s*.10))
    d.arc([int(s*.18), int(s*.05), int(s*.82), int(s*.60)], 180, 0, fill=W, width=lw)
    d.rectangle([int(s*.12), int(s*.44), int(s*.28), int(s*.68)], fill=W)
    d.rectangle([int(s*.72), int(s*.44), int(s*.88), int(s*.68)], fill=W)


def make_icon_image(icon_type, color=(255, 255, 255, 255), size=64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)
    if icon_type == "headset":
        _draw_headset(d, size, color)
    else:
        _draw_speaker(d, size, color)
    return img


def save_icon(icon_type, color_hex, path):
    r = int(color_hex[1:3], 16)
    g = int(color_hex[3:5], 16)
    b = int(color_hex[5:7], 16)
    make_icon_image(icon_type, color=(r, g, b, 255)).save(path)


ICON_PATHS = [
    os.path.join(BASE_DIR, "icon_0.png"),
    os.path.join(BASE_DIR, "icon_1.png"),
]

# Initiale Icons generieren (werden später überschrieben wenn Config geladen)
save_icon("speaker", "#ffffff", ICON_PATHS[0])
save_icon("headset",  "#ffffff", ICON_PATHS[1])


# ── PipeWire / PulseAudio ─────────────────────────────────────────────────────

def get_all_sinks():
    try:
        text = subprocess.run(["pactl", "list", "sinks"],
                              capture_output=True, text=True).stdout
    except Exception:
        return []
    sinks  = []
    blocks = re.split(r'^(?:Sink|Ziel) #\d+', text, flags=re.MULTILINE)[1:]
    for block in blocks:
        name = re.search(r'Name:\s*(\S+)', block)
        desc = re.search(r'(?:Beschreibung|Description):\s*(.+)', block)
        if name and desc:
            sinks.append((name.group(1).strip(), desc.group(1).strip()))
    return sinks


def get_default_sink():
    return subprocess.run(["pactl", "get-default-sink"],
                          capture_output=True, text=True).stdout.strip()


def set_sink(sink_name):
    subprocess.run(["pactl", "set-default-sink", sink_name])
    result = subprocess.run(["pactl", "list", "sink-inputs", "short"],
                            capture_output=True, text=True)
    for line in result.stdout.strip().splitlines():
        if line:
            subprocess.run(["pactl", "move-sink-input", line.split()[0], sink_name])


# ── Konfiguration ─────────────────────────────────────────────────────────────

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    return {"selected_sinks": [], "sink_icons": {}}


def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)


# ── Icon-Auswahl Widget ───────────────────────────────────────────────────────

CARD_CSS = b"""
.device-card {
    border: 2px solid #cccccc;
    border-radius: 8px;
    padding: 8px;
    background: white;
}
.device-card:checked { border-color: #1565c0; background: #e3f2fd; }
.device-card label { font-size: 11px; color: #222; }
.icon-btn { border-radius: 6px; padding: 4px; }
.icon-btn:checked { background: #bbdefb; border: 2px solid #1976d2; }
"""


def _pil_to_pixbuf(img):
    img = img.convert("RGBA")
    data = img.tobytes()
    return GdkPixbuf.Pixbuf.new_from_bytes(
        GLib_bytes(data), GdkPixbuf.Colorspace.RGB, True, 8,
        img.width, img.height, img.width * 4)


def pil_pixbuf(icon_type, size=32):
    from gi.repository import GLib
    img  = make_icon_image(icon_type, color=(40, 40, 40, 255), size=size)
    # Auf weißem Hintergrund
    bg   = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    bg.paste(img, mask=img)
    data = bg.tobytes()
    pb   = GdkPixbuf.Pixbuf.new_from_bytes(
        GLib.Bytes(data), GdkPixbuf.Colorspace.RGB,
        True, 8, size, size, size * 4)
    return pb


class IconChooser(Gtk.Box):
    """Zwei Toggle-Buttons: Lautsprecher | Headset"""
    def __init__(self, current="speaker"):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self._buttons = {}
        group = None
        for itype in ICON_TYPES:
            pb  = pil_pixbuf(itype, 28)
            img = Gtk.Image.new_from_pixbuf(pb)
            btn = Gtk.RadioButton.new_from_widget(group)
            if group is None:
                group = btn
            btn.set_image(img)
            btn.set_mode(False)          # nur Icon, kein Label
            btn.set_tooltip_text(ICON_LABELS[itype])
            btn.get_style_context().add_class("icon-btn")
            self._buttons[itype] = btn
            self.pack_start(btn, False, False, 0)
        self.set_value(current)

    def set_value(self, icon_type):
        if icon_type in self._buttons:
            self._buttons[icon_type].set_active(True)

    def get_value(self):
        for itype, btn in self._buttons.items():
            if btn.get_active():
                return itype
        return "speaker"


class DeviceCard(Gtk.Frame):
    def __init__(self, name, label_text, selected=False, icon_type="speaker"):
        super().__init__()
        self.sink_name = name
        self.get_style_context().add_class("device-card")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        self.add(vbox)

        # Checkbox + Gerätename
        self.check = Gtk.CheckButton(label=label_text)
        self.check.set_active(selected)
        self.check.get_child().set_max_width_chars(20)
        self.check.get_child().set_line_wrap(True)
        vbox.pack_start(self.check, False, False, 0)

        # Icon-Auswahl
        icon_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        icon_lbl = Gtk.Label(label="Icon:")
        icon_lbl.set_halign(Gtk.Align.START)
        icon_row.pack_start(icon_lbl, False, False, 0)
        self.icon_chooser = IconChooser(icon_type)
        icon_row.pack_start(self.icon_chooser, False, False, 0)
        vbox.pack_start(icon_row, False, False, 0)

    def get_active(self):
        return self.check.get_active()

    def set_active(self, val):
        self.check.set_active(val)

    def connect_toggled(self, cb):
        self.check.connect("toggled", cb)

    def get_icon_type(self):
        return self.icon_chooser.get_value()


# ── Einstellungen-Dialog ──────────────────────────────────────────────────────

class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent_app):
        super().__init__(title="Einstellungen – Audio-Ausgang")
        self.set_default_size(560, 340)
        self.set_resizable(True)
        self.parent_app = parent_app

        provider = Gtk.CssProvider()
        provider.load_from_data(CARD_CSS)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.add_buttons("Abbrechen", Gtk.ResponseType.CANCEL,
                         "Speichern",  Gtk.ResponseType.OK)

        box = self.get_content_area()
        box.set_spacing(12)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(12)
        box.set_margin_bottom(8)

        info = Gtk.Label()
        info.set_markup("<b>Gerät</b>   <small>(genau 2 auswählen, Icon je Gerät wählbar)</small>")
        info.set_halign(Gtk.Align.START)
        box.pack_start(info, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(200)
        box.pack_start(scroll, True, True, 0)

        self.flow = Gtk.FlowBox()
        self.flow.set_max_children_per_line(3)
        self.flow.set_min_children_per_line(2)
        self.flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flow.set_row_spacing(10)
        self.flow.set_column_spacing(10)
        self.flow.set_margin_top(6)
        self.flow.set_margin_bottom(6)
        scroll.add(self.flow)

        self.status_label = Gtk.Label(label="")
        self.status_label.set_halign(Gtk.Align.START)
        box.pack_start(self.status_label, False, False, 0)

        self.cards = []
        selected_set = set(parent_app.config.get("selected_sinks", []))
        sink_icons   = parent_app.config.get("sink_icons", {})

        for name, label in get_all_sinks():
            itype = sink_icons.get(name, "speaker")
            card  = DeviceCard(name, label,
                               selected=(name in selected_set),
                               icon_type=itype)
            card.connect_toggled(self._on_toggled)
            self.flow.add(card)
            self.cards.append(card)

        self._update_status()
        self.show_all()

    def _on_toggled(self, checkbox):
        card = next(c for c in self.cards if c.check is checkbox)
        if len(self._get_selected()) > 2:
            checkbox.handler_block_by_func(self._on_toggled)
            checkbox.set_active(False)
            checkbox.handler_unblock_by_func(self._on_toggled)
        self._update_status()

    def _update_status(self):
        n = len(self._get_selected())
        if n < 2:
            self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)
            self.status_label.set_markup(
                f"<span color='#c0392b'>Bitte genau 2 Ausgänge wählen ({n}/2)</span>")
        else:
            self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(True)
            self.status_label.set_markup("<span color='#27ae60'>✓ 2 Ausgänge gewählt</span>")

    def _get_selected(self):
        return [c.sink_name for c in self.cards if c.get_active()]

    def get_result(self):
        selected   = self._get_selected()
        sink_icons = {c.sink_name: c.get_icon_type() for c in self.cards}
        return selected, sink_icons


# ── Haupt-App ─────────────────────────────────────────────────────────────────

class AudioTray:
    def __init__(self):
        self.config       = load_config()
        self.all_sinks    = get_all_sinks()
        self.current_sink = get_default_sink()

        if len(self.config.get("selected_sinks", [])) < 2 and len(self.all_sinks) >= 2:
            self.config["selected_sinks"] = [self.all_sinks[0][0], self.all_sinks[1][0]]
            save_config(self.config)

        self._regenerate_icons()

        self.status_icon = XApp.StatusIcon()
        self.status_icon.set_visible(True)
        self.status_icon.connect("activate", self._on_click)

        self._update_icon()
        self._build_menu()

    def _regenerate_icons(self):
        sel        = self.config.get("selected_sinks", [])
        sink_icons = self.config.get("sink_icons", {})
        for i, sink in enumerate(sel[:2]):
            itype = sink_icons.get(sink, "speaker")
            save_icon(itype, "#ffffff", ICON_PATHS[i])

    def _selected(self):
        return self.config.get("selected_sinks", [])

    def _active_index(self):
        sel = self._selected()
        return sel.index(self.current_sink) if self.current_sink in sel else 0

    def _update_icon(self):
        idx  = self._active_index()
        path = ICON_PATHS[idx % len(ICON_PATHS)]
        self.status_icon.set_icon_name(path)
        sink_map = {n: l for n, l in self.all_sinks}
        self.status_icon.set_tooltip_text(
            f"Audio: {sink_map.get(self.current_sink, self.current_sink)}")

    def _build_menu(self):
        self._menu = Gtk.Menu()
        sink_map   = {n: l for n, l in self.all_sinks}
        first      = None
        for name in self._selected():
            label = sink_map.get(name, name)
            if first is None:
                item  = Gtk.RadioMenuItem(label=label)
                first = item
            else:
                item = Gtk.RadioMenuItem.new_with_label_from_widget(first, label)
            item.set_active(name == self.current_sink)
            item.connect("activate", self._on_sink_selected, name)
            self._menu.append(item)

        if self._selected():
            self._menu.append(Gtk.SeparatorMenuItem())

        s = Gtk.MenuItem(label="Einstellungen")
        s.connect("activate", self._on_settings)
        self._menu.append(s)
        self._menu.append(Gtk.SeparatorMenuItem())
        q = Gtk.MenuItem(label="Beenden")
        q.connect("activate", lambda _: Gtk.main_quit())
        self._menu.append(q)

        self._menu.show_all()
        self.status_icon.set_secondary_menu(self._menu)

    def _on_click(self, icon, button, time):
        if button == 1:
            sel = self._selected()
            if len(sel) < 2:
                return
            self._switch_to(sel[(self._active_index() + 1) % len(sel)])

    def _on_sink_selected(self, item, name):
        if item.get_active() and name != self.current_sink:
            self._switch_to(name)

    def _switch_to(self, sink_name):
        self.current_sink = sink_name
        set_sink(sink_name)
        self._update_icon()

    def _on_settings(self, _):
        dialog = SettingsDialog(self)
        if dialog.run() == Gtk.ResponseType.OK:
            selected, sink_icons = dialog.get_result()
            self.config["selected_sinks"] = selected
            self.config["sink_icons"]     = sink_icons
            save_config(self.config)
            self._regenerate_icons()
            self._update_icon()
            self._build_menu()
        dialog.destroy()


if __name__ == "__main__":
    AudioTray()
    Gtk.main()
