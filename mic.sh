#!/bin/bash                     

# Verificar el estado actual del micrófono
state=$(amixer get Capture | grep -o '\[on\]\|\[off\]' | head -n 1)

# Si está apagado, lo enciende, si está encendido, lo apaga
if [[ $state == "[off]" ]]; then
    amixer set Capture cap
else
    amixer set Capture nocap
fi
