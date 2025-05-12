#!/bin/bash
PKGS=(playerctl)
for pkg in "${PKGS[@]}"; do
    if ! pacman -Q $pkg &>/dev/null; then
        echo "Instalando $pkg..."
        sudo pacman -S --noconfirm $pkg
    else
        echo "$pkg ya está instalado."
    fi
done

if [ "$1" == "toggle" ]; then
    playerctl -p spotify play-pause
    sleep .3
    notify-send -t 1200 "Spotify ($(playerctl -p spotify status))" "$(playerctl -p spotify metadata --format '{{artist}} - {{title}}')"
    exit 0
fi


if [ "$1" == "next" ]; then
    playerctl -p spotify next
    exit 0
fi

if [ "$1" == "prev" ]; then
    playerctl -p spotify previous
    exit 0
fi