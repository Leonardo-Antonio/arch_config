# !bin/sh

if [ "$1" = "" ]; then
    echo "⚠️​ No version number label has been entered"
    exit 1
fi

git tag "$1"
git push origin "$1"

echo "✅ Tag "$1" created and pushed to origin"