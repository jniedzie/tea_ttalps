# !/bin/bash

git remote add upstream git@github.com:jniedzie/tea.git
git push origin main

cp .gitignore_user .gitignore
cp .github/README_user.md .github/README.md
