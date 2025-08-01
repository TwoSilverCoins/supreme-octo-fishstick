#!/bin/bash
while true; do
  python3 bot.py
  echo "Bot crashed... restarting in 5s"
  sleep 5
done
