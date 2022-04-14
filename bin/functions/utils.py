#!/usr/bin/env python3

def isint(s):
    try:
        int(s, 10)
    except ValueError:
        return False
    else:
        return True
