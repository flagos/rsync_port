#!/bin/sh

while true; do
  echo "Starting port sync at $(date)"
  python main.py
  echo "Sync finished. Sleeping for 60 seconds..."
  sleep 60
done
