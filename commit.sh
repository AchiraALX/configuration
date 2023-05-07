#!/bin/bash

commit_msg="$1"
if [[ -z "$commit_msg" ]]; then
  echo "Please provide a commit message as the first argument."
  exit 1
fi

git add --all
git reset ./backend/default ./l*1/*.cfg
git commit -m "$commit_msg"
git push

# So I finally got it..
