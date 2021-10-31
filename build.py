#! /usr/bin/env python3
# Not an official setup.py that uses setuptools, rather something quick that prepares the directory for build
import sys
import subprocess


t = subprocess.run(["pip", "freeze"], capture_output=True)
print(t)


with open('requirements.txt', 'r') as reqs:
    t = list(reqs)
    for i in t:
        print(i.split('\n')[0])




