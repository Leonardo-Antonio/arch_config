# !bin/bash

repos=("gen4-be-draws" "gen4-be-gmw-games" "gen4-be-kyc" "gen4-be-translations" "gen4-be-security-authenticacion" "gen4-be-security-authorization")

cd "$HOME/Projects/GDP/Microservices"
if [ "$1" = "rm" ]; then
    echo "Removing all repositories"
    rm -rf ${repos[*]}
    exit 0
fi

for repo in "${repos[@]}"; do
  echo "Cloning $repo"
  git clone http://git.gdpteam.com/4gen/$repo.git
  cd $repo
  git tag --sort=-creatordate | head -n 1 | xargs git checkout
  cd ..
done