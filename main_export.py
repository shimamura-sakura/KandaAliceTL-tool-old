#!/bin/env python3
import json
import struct
from common import FROOT, FNAME, NROOT, MAGIC

U32_3 = struct.Struct('<III')
U32_1 = struct.Struct('<I')


def process_file(in_filename, out_filename):
    out_data = []
    with open(in_filename, 'rb') as fp:
        assert fp.read(16) == MAGIC
        ins_len, str_len, off_len = U32_3.unpack(fp.read(16)[0:12])
        ins_data = fp.read(ins_len)
        str_data = fp.read(str_len)
        off_data = fp.read(off_len)
        for offset, in U32_1.iter_unpack(off_data):
            string = str_data[offset:str_data.index(b'\0', offset)]
            string = string.decode('cp932')
            out_data.append({'old': string, 'new': string})
    with open(out_filename, 'w') as fp:
        json.dump(out_data, fp, indent=4, ensure_ascii=False)


for name in FNAME:
    process_file(FROOT + name, NROOT + name + '.json')
