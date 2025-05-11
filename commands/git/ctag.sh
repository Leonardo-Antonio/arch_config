# !bin/sh

if [ "$1" = "" ]; then
    echo "⚠️​ No version number label has been entered"
    exit 1
fi

if [ "$2" = "" ]; then
    echo "⚠️​ No commit message has been entered"
    exit 1
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
git add .
git commit -m "$1"
git tag -a "$1" -m "$2"
git push origin "$BRANCH" "$1"
echo "✅ Tag $1 created and pushed to origin/$BRANCH"