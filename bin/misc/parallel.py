#!/usr/bin/env python3
import sys
import subprocess
from threading import Thread, Semaphore

sem = Semaphore(50)

def conversion(file):
    with sem:
        subprocess.run(f'cat {file} | ../bin/parse_f7_output.pl > {file}.processed', shell=True)

[program, *files] = sys.argv
for file in files:
    thread1 = Thread(target=conversion, args=(file,))
    thread1.start()
    print('Queued ' + file, flush=True)
