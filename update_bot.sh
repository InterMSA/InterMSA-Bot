#!/bin/sh
pwd
git checkout main
git fetch origin
# git fetch origin
# git pull origin main
git reset --hard 
# git checkout -b newbranch
git pull origin main
sleep 2
# systemctl restart botd
cd /home/jake/MSA-Bot
tmux kill-session -t MSA \; new-session -d -s MSA \; send-keys "python3 main.py" Enter
