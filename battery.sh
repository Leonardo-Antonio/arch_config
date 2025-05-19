#!/bin/bash

# Nivel mínimo de batería para alertar
THRESHOLD=20

# Obtener porcentaje de batería
BATTERY_LEVEL=$(cat /sys/class/power_supply/BAT0/capacity)
BATTERY_STATUS=$(cat /sys/class/power_supply/BAT0/status)

notify-send "⚠️ Batería baja" "Nivel actual: $BATTERY_LEVEL%" -u critical
if [[ "$BATTERY_STATUS" == "Discharging" && "$BATTERY_LEVEL" -le "$THRESHOLD" ]]; then
  notify-send "⚠️ Batería baja" "Nivel actual: $BATTERY_LEVEL%" -u critical
fi
