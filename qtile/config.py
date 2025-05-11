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

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "terminator"
myBrowser = "qutebrowser"  # My browser of choice

def get_mic_status():
    result = subprocess.run(['amixer', 'get', 'Capture'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if '[off]' in result.stdout:
        return '🎤 OFF'
    else:
        return '🎤 ON'

mic_status_widget = widget.GenPollText(
    func=get_mic_status, 
    update_interval=1, 
    font="Ubuntu Mono",
    background='#282828',  # Color de fondo del widget
    foreground='fff',  # Color del texto (blanco)
    padding=2,
    fontsize=14
)

keys = [
    # The essentials
    Key([mod], "Return",
        lazy.spawn(myTerm),
        desc='Launches My Terminal'
        ),

    Key([mod], "F11",
        lazy.spawn("flameshot gui"),
        desc='captura pantalla'
        ),


    Key([mod], "s",
        lazy.spawn(f"sh {Path.home()}/.config/rofi/launchers/type-3/launcher.sh"),
        desc='Show menu'
    ),

    Key([mod], "F1",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc='Launches My Terminal'
        ),

    Key([mod], "F2",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%"),
        desc='bajar vol'
        ),

    Key([mod], "F3",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%"),
        desc='subir vol'
        ),

    Key([mod], "F5",
        lazy.spawn("brightnessctl  set 10%+"),
        desc='subir brillo'
        ),

    Key([mod], "F4",
        lazy.spawn("brightnessctl  set 10%-"),
        desc='bajar brillo'
        ),

    Key([mod, "shift"], "Return",
        lazy.spawn("dmenu_run -p 'Run: '"),
        desc='Run Launcher'
        ),
    Key([mod], "b",
        lazy.spawn(myBrowser),
        desc='Qutebrowser'
        ),
    Key([mod], "Tab",
        lazy.next_layout(),
        desc='Toggle through layouts'
        ),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r",
        lazy.restart(),
        desc='Restart Qtile'
        ),
    Key([mod, "shift"], "q",
        lazy.shutdown(),
        desc='Shutdown Qtile'
        ),
    # Switch focus to specific monitor (out of three)
    Key([mod], "w",
        lazy.to_screen(0),
        desc='Keyboard focus to monitor 1'
        ),
    Key([mod], "e",
        lazy.to_screen(1),
        desc='Keyboard focus to monitor 2'
        ),
    Key([mod], "r",
        lazy.to_screen(2),
        desc='Keyboard focus to monitor 3'
        ),
    # Switch focus of monitors
    Key([mod], "period",
        lazy.next_screen(),
        desc='Move focus to next monitor'
        ),
    Key([mod], "comma",
        lazy.prev_screen(),
        desc='Move focus to prev monitor'
        ),
    # Treetab controls
    Key([mod, "shift"], "h",
        lazy.layout.move_left(),
        desc='Move up a section in treetab'
        ),
    Key([mod, "shift"], "l",
        lazy.layout.move_right(),
        desc='Move down a section in treetab'
        ),
    # Window controls
    Key([mod], "j",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'
        ),
    Key([mod], "k",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'
        ),
    Key([mod, "shift"], "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down(),
        desc='Move windows down in current stack'
        ),
    Key([mod, "shift"], "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up(),
        desc='Move windows up in current stack'
        ),
    Key([mod], "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
        ),
    Key([mod], "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
        ),
    Key([mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'
        ),
    Key([mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
        ),
    Key([mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
        ),
    Key([mod], "f",
        lazy.window.toggle_fullscreen(),
        desc='toggle fullscreen'
        ),
    # Stack controls
    Key([mod, "shift"], "Tab",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'
        ),
    Key([mod], "space",
        lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'
        ),
    Key([mod, "shift"], "space",
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'
        )
]

groups = [Group("BACK", layout='monadtall'),
          Group("FRONT", layout='monadtall'),
          Group("WEB", layout='monadtall'),
          Group("CHAT", layout='monadtall'),
          Group("DOC", layout='monadtall'),
          Group("MAIL", layout='monadtall'),
          Group("MUS", layout='monadtall'),
          Group("VID", layout='monadtall'),
          ]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 2,
                "margin": 2,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
        font="Ubuntu",
        fontsize=10,
        sections=["FIRST", "SECOND", "THIRD", "FOURTH"],
        section_fontsize=10,
        border_width=2,
        bg_color="1c1f24",
        active_bg="c678dd",
        active_fg="000000",
        inactive_bg="a9a1e1",
        inactive_fg="1c1f24",
        padding_left=0,
        padding_x=0,
        padding_y=5,
        section_top=10,
        section_bottom=20,
        level_shift=8,
        vspace=3,
        panel_width=200
    ),
    layout.Floating(**layout_theme)
]

colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=10,
    padding=2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()


def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth=0,
            padding=6,
            foreground=colors[2],
            background=colors[0]
        ),
        # widget.Image(
        #     filename="~/.config/qtile/icons/arch.png",
        #     scale="False",
        #     mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(myTerm)}
        # ),
        widget.Sep(
            linewidth=0,
            padding=6,
            foreground=colors[2],
            background=colors[0]
        ),
        widget.GroupBox(
            font="Ubuntu Bold",
            fontsize=9,
            margin_y=3,
            margin_x=0,
            padding_y=5,
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
            background=colors[0]
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[2],
            background=colors[0],
            padding=0,
            scale=0.7
        ),
        widget.CurrentLayout(
            foreground=colors[2],
            background=colors[0],
            padding=5
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        widget.WindowName(
            foreground=colors[2],
            background=colors[0],
            padding=5,
            fontsize=12
        ),
        mic_status_widget,
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        widget.Clock(
            foreground=colors[2],
            background=colors[0],
            format="%Y-%m-%d %a %I:%M %p"
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        widget.Systray(
            background=colors[0],
            icon_size=20
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        widget.Memory(
            foreground=colors[2],
            background=colors[0],
            fmt='Mem: {}',
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')}
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        widget.CPUGraph(
            width=50,
            height=40,
            border_color=colors[5],
            fill_color=colors[5],
            graph_color=colors[5],
            background=colors[0],
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        widget.Battery(
            foreground=colors[2],
            background=colors[0],
            format="Battery: {char} {percent:2.0%}",
            update_interval=10,
            low_percentage=0.2,
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e tlp-stat -b')}
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        widget.Volume(
            foreground=colors[2],
            background=colors[0],
            fmt="Vol: {}",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn("pavucontrol")}
        ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
        # widget.Network(
        #     foreground=colors[2],
        #     background=colors[0],
        #     format="Net: {down} ↓↑ {up}",
        #     interface="wlp2s0"
        # ),
        widget.TextBox(
            text='|',
            font="Ubuntu Mono",
            background=colors[0],
            foreground='474747',
            padding=2,
            fontsize=14
        ),
    ]
    return widgets_list


screens = [
    Screen(
        top=bar.Bar(
            init_widgets_list(), 24, background=colors[0]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["xbindkeys"])
    subprocess.Popen(["nm-applet &"])