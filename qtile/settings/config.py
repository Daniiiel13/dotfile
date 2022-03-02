# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from os import path
import subprocess

@hook.subscribe.startup_once
def autostart():
    subprocess.call([path.join(path.expanduser('~'), '.config', 'qtile', 'autostart.sh')])

def icon(foreground=["#000000", "#000000"], background="?",fontsize=16, text="?"):
    return widget.TextBox(
        foreground=foreground,
        background=background,
        fontsize=fontsize,
        text=text,
        padding=3
    )

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Toggle floating
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Menu
    Key([mod], "m", lazy.spawn("rofi -show drun")),
    Key([mod], "s", lazy.spawn("scrot")),
    Key([mod], "e", lazy.spawn("thunar")),

    # Browser
    Key([mod], "b", lazy.spawn("firefox")),

    # Window Nav
    Key([mod, "shift"], "m", lazy.spawn("rofi -show run")),

    # Volume
    #Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5")),
    #Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5")),
    #Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    Key([mod, "shift"], "r", lazy.spawn("redshift -x")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

]

groups = [Group(i) for i in ["爵 ", " ", " ", " ", " "," "]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layout_conf = {
    'border_focus': '#52b84c',
    'border_width': 1,
    'margin': 4
}

layouts = [
    layout.Columns(**layout_conf),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='UbuntuMono Nerd Font',
    fontsize=17,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    foreground=["#f1ffff", "#f1ffff"],
                    background=["#52b84c", "#52b84c"],
                    font='UbuntuMono Nerd Font',
                    fontsize=19,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=5,
                    borderwidth=1,
                    active=["#000000", "#000000"],
                    inactive=["#f1ffff", "#f1ffff"],
                    rounded=False,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=["#52b84c", "#52b84c"],
                    this_current_screen_border=["#217031", "#217031"],
                    this_screen_border=["#5c5c5c", "#5c5c5c"],
                    other_current_screen_border=["#254b30", "#254b30"],
                    other_screen_border=["#254b30", "#254b30"],
                    disable_drag=True
                ),
                widget.WindowName(
                    foreground=["#52b84c", "#52b84c"],
                    background=["#0f101a", "#0f101a"],
                    fontsize=16,
                    font='UbuntuMono Nerd Font',
                ),
                widget.Systray(),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile', 'img', 'bar4.png')
                ),
                icon(background=["#52b84c", "#52b84c"], text=' '),
                widget.CheckUpdates(
                    background=["#52b84c", "#52b84c"],
                    colour_have_updates=["#f1ffff", "#f1ffff"],
                    colour_no_updates=["#000000", "#000000"],
                    no_update_string='0',
                    display_format='{updates}',
                    update_interval=1800,
                    custom_command='checkupdates',
                ),
                icon(background=["#52b84c", "#52b84c"], text=' '),  # Icon: nf-fa-feed
                widget.Net(
                    foreground=["#000000", "#000000"],
                    background=["#52b84c", "#52b84c"],
                    interface='wlo1'
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile', 'img', 'bar2.png')
                ),
                widget.CurrentLayoutIcon(
                    background=["#cf2e2e", "#cf2e2e"],
                    scale=0.65
                ),
                widget.CurrentLayout(
                    foreground=["#000000", "#000000"],
                    background=["#cf2e2e", "#cf2e2e"],
                ),
                widget.Sep(
                    background=["#cf2e2e", "#cf2e2e"],
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile', 'img', 'bar3.png')
                ),
                widget.Clock(
                    foreground=["#0f101a", "#0f101a"],
                    background=["#52b84c", "#52b84c"],
                    format='%d/%m/%Y - %H:%M'
                    ),
                widget.TextBox(
                    foreground=["#0f101a", "#0f101a"],
                    background=["#52b84c", "#52b84c"],
                    padding=7,
                    text=''
                ),
            ],
            24,
            opacity=1
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
    # Segunda pantalla.
     Screen(
        top=bar.Bar(
            [
                  widget.GroupBox(
                    foreground=["#f1ffff", "#f1ffff"],
                    background=["#52b84c", "#52b84c"],
                    font='UbuntuMono Nerd Font',
                    fontsize=19,
                    margin_y=3,
                    margin_x=0,
                    padding_y=8,
                    padding_x=5,
                    borderwidth=1,
                    active=["#000000", "#000000"],
                    inactive=["#f1ffff", "#f1ffff"],
                    rounded=False,
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=["#52b84c", "#52b84c"],
                    this_current_screen_border=["#217031", "#217031"],
                    this_screen_border=["#5c5c5c", "#5c5c5c"],
                    other_current_screen_border=["#254b30", "#254b30"],
                    other_screen_border=["#254b30", "#254b30"],
                    disable_drag=True
                ),
                widget.WindowName(
                    foreground=["#52b84c", "#52b84c"],
                    background=["#0f101a", "#0f101a"],
                    fontsize=16,
                    font='UbuntuMono Nerd Font',
                ),
                widget.Image(
                    filename=path.join(path.expanduser('~'), '.config', 'qtile', 'img', 'bar1.png')
                ),
                widget.CurrentLayoutIcon(
                    background=["#cf2e2e", "#cf2e2e"],
                    scale=0.65
                ),
                widget.CurrentLayout(
                    foreground=["#000000", "#000000"],
                    background=["#cf2e2e", "#cf2e2e"],
                ),
                widget.Sep(
                    background=["#cf2e2e", "#cf2e2e"],
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
            ],
            24,
            opacity=1
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ], 
    border_focus='#52b84c'
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"
