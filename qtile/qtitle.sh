sudo pacman -S alsa-utils pulseaudio qtile python-pip python-setuptools rofi terminator flameshot brightnessctl feh qutebrowser dmenu xorg-xev xorg-xwininfo
mkdir -p ~/.config/qtile
rm ~/.config/qtile/config.py
ln -s ~/.config/utils/qtile/config.py ~/.config/qtile/config.py
qtile cmd-obj -o cmd -f restart