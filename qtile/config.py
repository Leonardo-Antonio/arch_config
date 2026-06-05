# -*- coding: utf-8 -*-
from libqtile.dgroups import simple_key_binder
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import (
    Click, Drag, Group, KeyChord, Key, Match, Screen, ScratchPad, DropDown,
)
from libqtile.lazy import lazy  # Corregido aquí
from libqtile import layout, bar, widget, hook
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401
from pathlib import Path

mod = "mod4"  # Sets mod key to SUPER/WINDOWS
myTerm = "terminator"
myBrowser = "qutebrowser"  # My browser of choice

# Fuentes centralizadas: usa Nerd Font para tener glifos de iconos.
# Requiere `ttf-cascadia-code-nerd` (o el paquete de CaskaydiaCove Nerd Font).
# Si faltan, cambialas aqui (un solo lugar) por otra Nerd Font instalada,
# p.ej. "JetBrainsMono Nerd Font" / "Iosevka Nerd Font".
FONT = "CaskaydiaCove Nerd Font Bold"
FONT_MONO = "CaskaydiaCove Nerd Font Mono"
FONT_MONO_BOLD = "CaskaydiaCove Nerd Font Mono Bold"

# Verde mas oscuro para el bloque de Spotify (en vez del verde brillante).
SPOTIFY_GREEN = "#34A146DF"

# Superficies para el estilo "powerline" de la barra (Tokyo Night Storm).
# Alternamos SURFACE1 (claro) / SURFACE2 (oscuro) entre grupos de widgets.
SURFACE0 = "#1a1b26"  # base de la barra
SURFACE1 = "#24283b"  # bloque claro
SURFACE2 = "#16161e"  # bloque oscuro
PL_ARROW = ""   # glifo flecha izquierda (Nerd Font powerline)


def get_mic_status():
    result = subprocess.run(
        ["amixer", "get", "Capture"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if "[off]" in result.stdout:
        return "󰍭 OFF"
    else:
        return "󰍬 ON"


# Ancho visible (en caracteres) de la ventana del titulo de Spotify.
NP_WIDTH = 20
# Separador que se ve entre el final y el inicio del texto al dar la vuelta.
NP_SEP = "   •   "
# Cada cuantos ticks se vuelve a consultar a playerctl (el scroll avanza en
# cada tick, pero la metadata solo se refresca cada NP_REFRESH ticks).
NP_REFRESH = 12
# Estado persistente del marquee entre llamadas.
_np = {"meta": "", "status": "", "pos": 0, "tick": 0}


def get_now_playing():
    """Cancion actual de Spotify con efecto marquee (scroll derecha->izq).

    GenPollText llama esta funcion cada `update_interval` segundos; en cada
    llamada avanzamos un caracter la ventana visible, dando el efecto carrusel.
    Si el titulo cabe en NP_WIDTH no se desplaza.
    """
    try:
        # Refrescar metadata solo cada NP_REFRESH ticks (playerctl es costoso).
        if _np["tick"] % NP_REFRESH == 0:
            status = subprocess.run(
                ["playerctl", "-p", "spotify", "status"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=1,
            ).stdout.strip()
            if status not in ("Playing", "Paused"):
                _np.update(meta="", icon="", pos=0, tick=0)
                return ""
            meta = subprocess.run(
                ["playerctl", "-p", "spotify", "metadata", "--format",
                 "{{artist}} - {{title}}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=1,
            ).stdout.strip()
            # Si cambia la cancion, reiniciar el scroll desde el inicio.
            if meta != _np["meta"]:
                _np["pos"] = 0
            _np["meta"], _np["status"] = meta, status

        _np["tick"] += 1
        status, meta = _np["status"], _np["meta"]
        if not meta:
            return ""
        icon = "" if status == "Playing" else "󰖁"
        # Titulo corto: sin scroll, ancho fijo para que la barra no "salte".
        if len(meta) <= NP_WIDTH:
            return f"{icon} {meta.ljust(NP_WIDTH)}"
        # Titulo largo: ventana deslizante sobre texto+separador, en bucle.
        full = meta + NP_SEP
        pos = _np["pos"] % len(full)
        window = (full + full)[pos:pos + NP_WIDTH]
        _np["pos"] = pos + 1
        return f"{icon} {window}"
    except Exception:
        return ""


mic_status_widget = widget.GenPollText(
    func=get_mic_status,
    update_interval=1,
    font=FONT_MONO,
    background=SURFACE1,  # Color de fondo del widget
    foreground="#c0caf5",  # Color del texto
    padding=6,
    fontsize=14,
)

keys = [
    # The essentials
    Key([mod], "Return", lazy.spawn(myTerm), desc="Launches My Terminal"),
    Key(
        [mod],
        "F11",
        lazy.spawn("env XDG_SESSION_TYPE=x11 flameshot gui"),
        desc="captura pantalla",
    ),
    Key(
        [mod],
        "s",
        lazy.spawn(f"sh {Path.home()}/.config/rofi/launchers/type-3/launcher.sh"),
        desc="Show menu",
    ),
    Key(
        [mod],
        "o",
        lazy.spawn(f"sh {Path.home()}/.config/rofi/rofi__file.sh"),
        desc="Show menu",
    ),
    Key(
        [mod],
        "c",
        lazy.spawn(f"setsid /opt/discord/discord >/dev/null 2>&1 &"),
        desc="Show menu",
    ),
    Key(
        [mod],
        "F1",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Launches My Terminal",
    ),
    Key(
        [mod],
        "F2",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"),
        desc="bajar vol",
    ),
    Key(
        [mod],
        "F3",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"),
        desc="subir vol",
    ),
    Key([mod], "F5", lazy.spawn("brightnessctl  set 10%+"), desc="subir brillo"),
    Key([mod], "F4", lazy.spawn("brightnessctl  set 10%-"), desc="bajar brillo"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.spawn("dmenu_run -p 'Run: '"),
        desc="Run Launcher",
    ),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Qutebrowser"),
    # Scratchpad: terminal flotante tipo dropdown (toggle)
    Key(
        [mod],
        "t",
        lazy.group["scratchpad"].dropdown_toggle("term"),
        desc="Toggle terminal flotante (scratchpad)",
    ),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle through layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Switch focus to specific monitor (out of three)
    Key([mod], "w", lazy.to_screen(0), desc="Keyboard focus to monitor 1"),
    Key([mod], "e", lazy.to_screen(1), desc="Keyboard focus to monitor 2"),
    Key([mod], "r", lazy.to_screen(2), desc="Keyboard focus to monitor 3"),
    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Move focus to prev monitor"),
    # Treetab controls
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.move_left(),
        desc="Move up a section in treetab",
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.move_right(),
        desc="Move down a section in treetab",
    ),
    # Window controls
    Key([mod], "j", lazy.layout.down(), desc="Move focus down in current stack pane"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up in current stack pane"),
    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down(),
        desc="Move windows down in current stack",
    ),
    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up(),
        desc="Move windows up in current stack",
    ),
    Key(
        [mod],
        "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc="Shrink window (MonadTall), decrease number in master pane (Tile)",
    ),
    Key(
        [mod],
        "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc="Expand window (MonadTall), increase number in master pane (Tile)",
    ),
    Key([mod], "n", lazy.layout.normalize(), desc="normalize window size ratios"),
    Key(
        [mod],
        "m",
        lazy.layout.maximize(),
        desc="toggle window between minimum and maximum sizes",
    ),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    # Stack controls
    Key(
        [mod, "shift"],
        "Tab",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc="Switch which side main pane occupies (XmonadTall)",
    ),
    Key(
        [mod],
        "space",
        lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack",
    ),
    Key(
        [mod, "shift"],
        "space",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
]

groups = [
    Group("󰧑 IA", layout="max"),
    Group("󰒍 BACK", layout="max"),
    Group("󰖟 FRONT", layout="max"),
    Group("󰈹 WEB", layout="max"),
    Group("󰙨 TEST", layout="max"),
    Group("󰆼 DB", layout="max"),
    Group("󰈙 DOC", layout="max"),
    Group("󰭹 CHAT", layout="max"),
]

# Scratchpad: terminal flotante que aparece/desaparece con mod+t (tipo Guake).
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term",
                myTerm,
                width=0.6,
                height=0.55,
                x=0.2,
                y=0.15,
                opacity=0.95,
                on_focus_lost_hide=True,
            ),
        ],
    )
)

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {
    "border_width": 2,
    "margin": 3,
    "border_focus": "7aa2f7",
    "border_normal": "16161e",
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.Stack(num_stacks=2),
    # layout.RatioTile(**layout_theme),
    # layout.TreeTab(
    #     font="Ubuntu",
    #     fontsize=10,
    #     sections=["FIRST", "SECOND", "THIRD", "FOURTH"],
    #     section_fontsize=10,
    #     border_width=2,
    #     bg_color="1c1f24",
    #     active_bg="c678dd",
    #     active_fg="000000",
    #     inactive_bg="a9a1e1",
    #     inactive_fg="1c1f24",
    #     padding_left=0,
    #     padding_x=0,
    #     padding_y=5,
    #     section_top=10,
    #     section_bottom=20,
    #     level_shift=8,
    #     vspace=3,
    #     panel_width=200
    # ),
    # layout.Floating(**layout_theme)
]

# Tokyo Night
colors = [
    ["#1a1b26", "#1a1b26"],  # 0 base / fondo barra
    ["#16161e", "#16161e"],  # 1 mas oscuro
    ["#c0caf5", "#c0caf5"],  # 2 texto
    ["#a30c28", "#a30c28"],  # 3 rojo
    ["#9ece6a", "#9ece6a"],  # 4 verde
    ["#ff9e64", "#ff9e64"],  # 5 naranja
    ["#7aa2f7", "#7aa2f7"],  # 6 azul
    ["#bb9af7", "#bb9af7"],  # 7 magenta
    ["#7dcfff", "#7dcfff"],  # 8 cyan
    ["#9d7cd8", "#9d7cd8"],  # 9 purpura
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(font=FONT, fontsize=10, padding=2, background=colors[2])
extension_defaults = widget_defaults.copy()


def powerline(fg, bg):
    """Transicion 'powerline': flecha cuyo color (fg) es el bloque de la
    DERECHA y el fondo (bg) es el bloque de la IZQUIERDA."""
    return widget.TextBox(
        text=PL_ARROW,
        font=FONT_MONO,
        fontsize=33,
        padding=0,
        foreground=fg,
        background=bg,
    )


def spot_btn(icon, action, bg):
    return widget.TextBox(
        text=icon,
        font=FONT_MONO_BOLD,
        background=bg,
        foreground="#1a1b26",
        padding=5,
        fontsize=20,
        mouse_callbacks={
            "Button1": lambda: qtile.spawn(
                f'{os.getenv("HOME")}/.config/utils/control_audio_spotify.sh {action}'
            )
        },
    )


def init_widgets_list():
    spotify_bg = SPOTIFY_GREEN  # verde mas oscuro para el bloque de Spotify
    widgets_list = [
        # ---------- IZQUIERDA (plano sobre la base) ----------
        widget.Sep(linewidth=0, padding=6, background=SURFACE0),
        widget.GroupBox(
            font=FONT,
            fontsize=10,
            margin_y=3,
            margin_x=0,
            padding_y=3,
            padding_x=3,
            borderwidth=3,
            active=colors[2],
            inactive=colors[7],
            rounded=False,
            highlight_color=colors[1],
            highlight_method="line",
            this_current_screen_border=colors[6],
            this_screen_border=colors[4],
            other_current_screen_border=colors[6],
            other_screen_border=colors[4],
            foreground=colors[2],
            background=SURFACE0,
        ),
        widget.CurrentLayout(
            mode="icon",
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[2],
            background=SURFACE0,
            padding=4,
            scale=0.7,
        ),
        widget.CurrentLayout(
            mode="text", foreground=colors[2], background=SURFACE0, padding=5,
        ),
        widget.WindowName(
            foreground=colors[2], background=SURFACE0, padding=5,
            fontsize=13, font=FONT, max_chars=60,
        ),

        # ---------- BLOQUE: SPOTIFY (verde) ----------
        powerline(spotify_bg, SURFACE0),
        spot_btn("󰒮", "prev", spotify_bg),
        spot_btn("󰐎", "toggle", spotify_bg),
        spot_btn("󰒭", "next", spotify_bg),
        widget.GenPollText(
            func=get_now_playing,
            update_interval=0.3,  # ritmo del scroll del marquee (mas bajo = mas fluido)
            font=FONT_MONO_BOLD,
            background=spotify_bg,
            foreground="#1a1b26",
            padding=3,
            fontsize=16,
            mouse_callbacks={
                "Button1": lambda: qtile.spawn(
                    f'{os.getenv("HOME")}/.config/utils/control_audio_spotify.sh toggle'
                )
            },
        ),

        # ---------- BLOQUE: SISTEMA (CPU temp + grafica + RAM) ----------
        powerline(SURFACE2, spotify_bg),
        widget.TextBox(
            text="󰔏", font=FONT_MONO, foreground=colors[5],
            background=SURFACE2, padding=4, fontsize=16,
        ),
        widget.ThermalSensor(
            font=FONT_MONO,
            foreground=colors[5], background=SURFACE2, fontsize=14,
            format="{temp:>2.0f}{unit}", update_interval=5,
            threshold=80, foreground_alert=colors[3],
        ),
        widget.TextBox(
            text="󰻠", font=FONT_MONO, foreground=colors[5],
            background=SURFACE2, padding=2, fontsize=16,
        ),
        widget.CPUGraph(
            width=55, height=24, line_width=1,
            border_color=SURFACE2, fill_color=colors[5],
            graph_color=colors[5], background=SURFACE2, margin_y=5,
        ),
        widget.Memory(
            font=FONT_MONO,
            foreground=colors[2], background=SURFACE2, fontsize=14,
            fmt="󰍛 {}", format="{MemUsed:>5.0f}{mm}",
            mouse_callbacks={"Button1": lambda: qtile.spawn(myTerm + " -e htop")},
        ),

        # ---------- BLOQUE: RED (ancho fijo -> no salta) ----------
        # widget.Net(
        #     font=FONT_MONO,
        #     foreground=colors[8], background=SURFACE1, fontsize=13,
        #     format="󰇚 {down:>5}{down_suffix}  {up:>5}{up_suffix} 󰕒",
        # ),

        # ---------- BLOQUE: ACTUALIZACIONES ----------
        # powerline(SURFACE2, SURFACE1),
        # widget.CheckUpdates(
        #     font=FONT_MONO,
        #     distro="Arch",
        #     display_format="󰚰 {updates}",
        #     no_update_string="󰄬 0",
        #     update_interval=1800,
        #     colour_have_updates=colors[5],
        #     colour_no_updates=colors[4],
        #     background=SURFACE2,
        #     fontsize=14,
        #     mouse_callbacks={
        #         "Button1": lambda: qtile.spawn(myTerm + " -e yay -Syu")
        #     },
        # ),

        # ---------- BLOQUE: AUDIO (volumen + microfono) ----------
        powerline(SURFACE1, SURFACE2),
        widget.Volume(
            font=FONT_MONO,
            foreground=colors[8], background=SURFACE1, fontsize=14,
            fmt="󰕾 {:>4}",
            mouse_callbacks={"Button1": lambda: qtile.spawn("pavucontrol")},
        ),
        mic_status_widget,

        # ---------- BLOQUE: BATERIA ----------
        powerline(SURFACE2, SURFACE1),
        widget.Battery(
            font=FONT_MONO,
            fontsize=14, foreground=colors[4], background=SURFACE2,
            format="{char} {percent:>4.0%}",
            charge_char="󰂄", discharge_char="󰁹", full_char="󰁹",
            empty_char="󰂎", unknown_char="󰁹",
            update_interval=10, low_percentage=0.2, low_foreground=colors[3],
        ),

        # ---------- BLOQUE: RELOJ ----------
        powerline(SURFACE1, SURFACE2),
        widget.Clock(
            font=FONT_MONO,
            fontsize=14, foreground=colors[2], background=SURFACE1,
            format="󰥔 %a %d %b  %I:%M %p",
        ),

        # ---------- BANDEJA + APAGADO ----------
        powerline(SURFACE2, SURFACE1),
        widget.Systray(background=SURFACE2, icon_size=18, padding=6),
        powerline(colors[3][0], SURFACE2),
        widget.TextBox(
            text="⏻", font=FONT, foreground="#fcfcff", 
            background=colors[3], padding=8, fontsize=12,
            mouse_callbacks={
                "Button1": lambda: qtile.spawn(
                    f'{os.getenv("HOME")}/.config/utils/powermenu_qtile.sh'
                )
            },
        ),
    ]
    return widgets_list


screens = [
    Screen(
        top=bar.Bar(
            init_widgets_list(),
            34,
            background=colors[0],
            margin=[3, 3, 1, 3],  # [arriba, derecha, abajo, izquierda]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["feh", "--bg-fill", os.path.expanduser("~/.config/utils/wallpapers/clasic.jpg")])
    subprocess.Popen(["xbindkeys"])
    subprocess.Popen(['picom', '--backend', 'glx', '--experimental-backends'])
    subprocess.Popen(["nm-applet"])
