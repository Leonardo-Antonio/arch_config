# !bin/sh

git fetch origin
echo "Last tag: "
if [ "$1" = "dev" ]; then
    git tag --sort=-creatordate | head -n 1 | xargs echo "🔥 TAG: "
else
    git tag --sort=-creatordate | head -n 20 | grep -v "dev" | head -n 1 | xargs echo "🔥 TAG: "
fi