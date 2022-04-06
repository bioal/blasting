#!/usr/bin/env python3
import sys
import subprocess
from threading import Thread, Semaphore

sem = Semaphore(50)

def conversion(file):
    with sem:
        subprocess.run(f'cat {file} | ../bin/perl/extract_top.pl > {file}.top 2> {file}.top.err', shell=True)

[program, *files] = sys.argv
for file in files:
    thread1 = Thread(target=conversion, args=(file,))
    thread1.start()
    print('Queued ' + file, flush=True)
