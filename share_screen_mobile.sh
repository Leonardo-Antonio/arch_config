PKGS=(android-tools scrcpy usbutils)
for pkg in "${PKGS[@]}"; do
    if ! pacman -Q $pkg &>/dev/null; then
        echo "Instalando $pkg..."
        sudo pacman -S --noconfirm $pkg
    else
        echo "$pkg ya está instalado."
    fi
done


RULE='SUBSYSTEM=="usb", ATTR{idVendor}=="0e8d", MODE="0666", GROUP="plugdev"'
echo "$RULE" | sudo tee /etc/udev/rules.d/51-android.rules > /dev/null
sudo udevadm control --reload-rules
sudo udevadm trigger
adb kill-server
adb start-server
adb devices
scrcpy