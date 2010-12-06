#!/usr/bin/env python

import sys, subprocess

if sys.platform == 'win32':
    pyargs = ['-u'] # binary mode
else:
    pyargs = []

solver = [sys.executable] + pyargs + [
    'solver.py',
    #'-v', '-f', 'debug.txt'
]

cmd = [
    sys.executable, '../abbots/client.py', '-s', 'munkeliv.ath.cx',
    '--iama=BFG9001', '--',
] + solver
subprocess.call(cmd)

print 'Debug output:'
print open('debug.txt').read()
