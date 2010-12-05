#!/usr/bin/env python

import sys, subprocess

cmd = [
    sys.executable, '../abbots/client.py', '-s', 'munkeliv.ath.cx', '--',
    sys.executable, 'solver.py', '-v', '-f', 'debug.txt',
]
subprocess.call(cmd)

print 'Debug output:'
print open('debug.txt').read()
