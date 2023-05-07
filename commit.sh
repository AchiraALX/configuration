#!/bin/bash

commit_msg="$1"
if [[ -z "$commit_msg" ]]; then
  echo "Please provide a commit message as the first argument."
  exit 1
fi

git add --all
git reset ./w*1/d*t ./w*2/d*t ./l*1/*.cfg
git commit -m "$commit_msg"
git push

# So I finally got it..
