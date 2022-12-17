#!/bin/env python3
import json
from common import FNAME, NROOT, MAGIC


def get_setB():
    used_chars = set()
    for name in FNAME:
        with open(NROOT + name + '.json', 'r') as fp:
            jdat = json.load(fp)
        for obj in jdat:
            used_chars.update(obj['new'])
    return used_chars
