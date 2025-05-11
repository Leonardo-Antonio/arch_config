sudo pacman -S sxhkd
mkdir -p ~/.config/sxhkd
touch ~/.config/sxhkd/sxhkdrc
cat shortcuts.txt > ~/.config/sxhkd/sxhkdrc
echo "sxhkd &" >> ~/.zshrc
source ~/.zshrc