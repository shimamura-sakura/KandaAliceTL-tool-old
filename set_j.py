#!/bin/env python3
import json
import struct
from common import FPATH_MAIN

U16_LE = struct.Struct('<H')
FILE_TO_VM = 0x80003cf
BEGIN_VOFF = 0x0814ae98
BEGIN_FOFF = BEGIN_VOFF - FILE_TO_VM


def get_setJ():
    jis_chars = set()
    jis_offst = dict()

    with open(FPATH_MAIN, 'rb') as fp:
        fdata = fp.read()
    with open('cp932-unicode.json', 'r') as fp:
        pairs = json.load(fp)

    file_off = BEGIN_FOFF
    for code_jis, code_u16 in pairs:
        if code_jis < 0x8140:
            continue

        curr_off = None
        curr_dat = None
        while True:
            file_u16 = U16_LE.unpack(fdata[file_off:file_off+2])[0]
            file_off = file_off+2
            if file_u16 == code_u16:
                curr_off = file_off - 2
                curr_dat = fdata[curr_off:curr_off+2]
                break
        curr_chr = curr_dat.decode('utf-16le')
        # print('F', hex(curr_off),
        #       'V', hex(curr_off + FILE_TO_VM),
        #       'J', hex(code_jis),
        #       'U', hex(code_u16))
        jis_chars.add(curr_chr)
        jis_offst[code_jis] = curr_off
    return jis_chars, jis_offst
