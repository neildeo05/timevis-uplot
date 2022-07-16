#!/usr/bin/env zsh
# This is the command if the file is not preprocessed python3 timevis.py --filename='10m.csv' --force='y'

set -xe

FILENAME="foo.csv"
FORCE=1

if [[ "${FORCE}" ]]; then
    
    python --version
    python timevis.py --filename=$FILENAME --force='y' --center_radius_mode='y' 
else
    python --version
    python timevis.py --filename=$FILENAME --force='n' --center_radius_mode='y'
fi
