#!/usr/bin/env bash
#
# Power / session menu para qtile + GDM.
# Reutiliza el tema rofi de adi1090x (powermenu/type-1) para mantener el look.
#
# Opciones: Lock · Suspend · Logout · Switch User · Reboot · Shutdown

dir="$HOME/.config/rofi/powermenu/type-1"
theme="style-1"

uptime="$(uptime -p | sed -e 's/up //g')"
host="$(hostname)"

# Iconos (usan los glifos del tema original)
lock='  Lock'
suspend='  Suspend'
logout='  Logout'
switch='  Switch User'
reboot='  Reboot'
shutdown='  Shutdown'
yes='  Yes'
no='  No'

rofi_cmd() {
	rofi -dmenu \
		-p "$host" \
		-mesg "Uptime: $uptime" \
		-theme "${dir}/${theme}.rasi"
}

confirm_cmd() {
	rofi -theme-str 'window {location: center; anchor: center; fullscreen: false; width: 250px;}' \
		-theme-str 'mainbox {children: [ "message", "listview" ];}' \
		-theme-str 'listview {columns: 2; lines: 1;}' \
		-theme-str 'element-text {horizontal-align: 0.5;}' \
		-theme-str 'textbox {horizontal-align: 0.5;}' \
		-dmenu \
		-p 'Confirmation' \
		-mesg 'Are you Sure?' \
		-theme "${dir}/${theme}.rasi"
}

confirm_exit() {
	echo -e "$yes\n$no" | confirm_cmd
}

run_menu() {
	echo -e "$lock\n$suspend\n$logout\n$switch\n$reboot\n$shutdown" | rofi_cmd
}

# Cierra la sesión de qtile (vuelve a GDM)
qtile_logout() {
	qtile cmd-obj -o cmd -f shutdown 2>/dev/null || loginctl terminate-session "${XDG_SESSION_ID}"
}

# Cambiar de usuario: en GDM no hay "fast user switch" por CLI, así que
# levantamos una nueva pantalla de login de GDM en otro VT manteniendo,
# si es posible, la sesión actual. Si falla, hacemos logout a GDM.
switch_user() {
	if command -v gdmflexiserver &>/dev/null; then
		gdmflexiserver
	elif command -v dm-tool &>/dev/null; then
		dm-tool switch-to-greeter
	else
		# GDM moderno: pedir un nuevo greeter vía systemd/logind.
		# Como fallback fiable, cerramos sesión y volvemos al selector de GDM.
		qtile_logout
	fi
}

lock_session() {
	if command -v betterlockscreen &>/dev/null; then
		betterlockscreen -l
	elif command -v i3lock &>/dev/null; then
		i3lock
	else
		loginctl lock-session "${XDG_SESSION_ID}"
	fi
}

chosen="$(run_menu)"
case "${chosen}" in
	"$lock")     lock_session ;;
	"$suspend")  systemctl suspend ;;
	"$logout")   [[ "$(confirm_exit)" == "$yes" ]] && qtile_logout ;;
	"$switch")   switch_user ;;
	"$reboot")   [[ "$(confirm_exit)" == "$yes" ]] && systemctl reboot ;;
	"$shutdown") [[ "$(confirm_exit)" == "$yes" ]] && systemctl poweroff ;;
esac
