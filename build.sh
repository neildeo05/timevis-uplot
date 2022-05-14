#!/usr/bin/env zsh
# This is the command if the file is not preprocessed python3 timevis.py --filename='10m.csv' --force='y'

set -xe

if [[ "${FORCE}" ]]; then
    python timevis.py --filename='10m.csv' --force='y' --center_radius_mode='y'
else
  python --version
    python3 timevis.py --filename='10m.csv' --force='n' --center_radius_mode='y'
fi
