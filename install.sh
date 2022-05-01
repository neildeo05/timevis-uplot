#!/usr/bin/env bash

cat requirements.txt | xargs -n 1 pip install
