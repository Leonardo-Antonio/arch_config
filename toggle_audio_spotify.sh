#!/bin/bash

# Buscar el ID del sink input de Spotify
spotify_id=$(pactl list sink-inputs | awk '
  /^Sink Input/ {gsub("#", "", $3); id = $3; found = 0}
  /application.name = "Spotify"/ {found = 1}
  found && id {print id; exit}
')

# Si no se encontró Spotify
if [[ -z "$spotify_id" ]]; then
  notify-send "Spotify no está reproduciendo audio."
  exit 1
fi

# Verificar el estado de mute actual
mute_status=$(pactl list sink-inputs | awk -v target="$spotify_id" '
  $1 == "Sink" && $2 == "Input" && $3 == "#"target {found=1}
  found && /Mute:/ {print $2; exit}
')

# Toggle
if [[ "$mute_status" == "yes" ]]; then
  pactl set-sink-input-mute "$spotify_id" 0
  notify-send "🔊 Spotify desmuteado."
else
  pactl set-sink-input-mute "$spotify_id" 1
  notify-send "🔇 Spotify muteado."
fi
