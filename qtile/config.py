# -*- coding: utf-8 -*-
from libqtile.dgroups import simple_key_binder
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.lazy import lazy  # Corregido aquí
from libqtile import layout, bar, widget, hook
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401
from libqtile.utils import guess_terminal
from pathlib import Path
import subprocess

mod = "mod4"  # Sets mod key to SUPER/WINDOWS
myTerm = "terminator"
myBrowser = "qutebrowser"  # My browser of choice

# Fuentes centralizadas: usa Nerd Font para tener glifos de iconos.
# Requiere `ttf-cascadia-code-nerd` (o el paquete de CaskaydiaCove Nerd Font).
# Si faltan, cambialas aqui (un solo lugar) por otra Nerd Font instalada,
# p.ej. "JetBrainsMono Nerd Font" / "Iosevka Nerd Font".
FONT = "CaskaydiaCove Nerd Font Bold"
FONT_MONO = "CaskaydiaCove Nerd Font Mono"


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


mic_status_widget = widget.GenPollText(
    func=get_mic_status,
    update_interval=1,
    font=FONT_MONO,
    background="#1a1b26",  # Color de fondo del widget
    foreground="#c0caf5",  # Color del texto
    padding=2,
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
    ["#f7768e", "#f7768e"],  # 3 rojo
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


def init_widgets_list():
    widgets_list = [
        widget.Sep(linewidth=0, padding=6, foreground=colors[2], background=colors[0]),
        # widget.Image(
        #     filename="~/.config/qtile/icons/arch.png",
        #     scale="False",
        #     mouse_callbacks={'Button1': lambda: qtile.spawn(myTerm)}
        # ),
        widget.Sep(linewidth=0, padding=6, foreground=colors[2], background=colors[0]),
        widget.GroupBox(
            font=FONT,
            fontsize=11,
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
            background=colors[0],
        ),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.CurrentLayout(
            mode="icon",
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[2],
            background=colors[0],
            padding=0,
            scale=0.7,
        ),
        widget.CurrentLayout(
            mode="text", foreground=colors[2], background=colors[0], padding=5,
        ),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.WindowName(
            foreground=colors[2], background=colors[0], padding=5, fontsize=13, font=FONT
        ),
        mic_status_widget,
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.TextBox(
            text="󰒮",
            font=FONT_MONO,
            background="#9ece6a",
            foreground="#1a1b26",
            padding=6,
            fontsize=18,
            mouse_callbacks={
                "Button1": lambda: qtile.spawn(
                    f'{os.getenv("HOME")}/.config/utils/control_audio_spotify.sh prev'
                )
            },
        ),
        widget.TextBox(
            text="󰐎",
            font=FONT_MONO,
            background="#9ece6a",
            foreground="#1a1b26",
            padding=6,
            fontsize=18,
            mouse_callbacks={
                "Button1": lambda: qtile.spawn(
                    f'{os.getenv("HOME")}/.config/utils/control_audio_spotify.sh toggle'
                )
            },
        ),
        widget.TextBox(
            text="󰒭",
            font=FONT_MONO,
            background="#9ece6a",
            foreground="#1a1b26",
            padding=6,
            fontsize=18,
            mouse_callbacks={
                "Button1": lambda: qtile.spawn(
                    f'{os.getenv("HOME")}/.config/utils/control_audio_spotify.sh next'
                )
            },
        ),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.Clock(
            fontsize=15,
            foreground=colors[2],
            background=colors[0],
            format="󰥔 %Y-%m-%d %a %I:%M %p",
        ),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.Systray(background=colors[0], icon_size=20),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.Memory(
            foreground=colors[2],
            background=colors[0],
            fontsize=14,
            fmt="󰍛 {}",
            mouse_callbacks={"Button1": lambda: qtile.spawn(myTerm + " -e htop")},
        ),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.TextBox(
            text="󰻠",
            font=FONT_MONO,
            foreground=colors[5],
            background=colors[0],
            padding=2,
            fontsize=16,
        ),
        widget.CPUGraph(
            width=60,
            height=50,
            border_color=colors[5],
            fill_color=colors[5],
            graph_color=colors[5],
            background=colors[0],
        ),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.Battery(
            fontsize=15,
            foreground=colors[2],
            background=colors[0],
            format="󰁹 {percent:2.0%}",
            update_interval=10,
            low_percentage=0.2,
        ),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.Volume(
            foreground=colors[2],
            background=colors[0],
            fontsize=14,
            fmt="󰕾 {}",
            mouse_callbacks={"Button1": lambda: qtile.spawn("pavucontrol")},
        ),
        # widget.Network(
        #     foreground=colors[2],
        #     background=colors[0],
        #     format="Net: {down} ↓↑ {up}",
        #     interface="wlp2s0"
        # ),
        widget.TextBox(
            text="|",
            font=FONT_MONO,
            background=colors[0],
            foreground="#414868",
            padding=2,
            fontsize=14,
        ),
        widget.TextBox(
            text="⏻",
            font=FONT_MONO,
            foreground=colors[3],
            background=colors[0],
            padding=6,
            fontsize=18,
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
    subprocess.Popen(["nm-applet &"])
