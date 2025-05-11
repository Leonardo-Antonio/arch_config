# !bin/sh

if [ "$1" = "" ]; then
    echo "⚠️​ No commit message has been entered"
    exit 1
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
git add . && git commit -m "$1" && git push origin "$BRANCH"

echo "✅ Commit "$1" created and pushed to origin/$BRANCH"