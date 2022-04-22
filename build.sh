#!/usr/bin/env zsh
# This is the command if the file is not preprocessed python3 timevis.py --filename='10m.csv' --force='y'

set -xe
if [[ "${PYENV}" ]]; then
  echo "foo"
  pyenv exec python timevis.py --filename='10m.csv' --force='n' --center_radiuys_mode'y'
else
  python3 timevis.py --filename='10m.csv' --force='n' --center_radius_mode='y'
fi

