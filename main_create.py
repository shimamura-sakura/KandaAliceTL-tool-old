#!/bin/env python3
import json
import struct
import set_j
import set_a
import set_b
from common import MAGIC, FROOT, FNAME, NROOT, OROOT, FPATH_MAIN

U16_BE = struct.Struct('>H')
U16_LE = struct.Struct('<H')
U32_3 = struct.Struct('<III')
U32_LE1 = struct.Struct('<I')

setJ, offJ = set_j.get_setJ()
setA = set_a.get_setA()
setB = set_b.get_setB()
setC = setJ - setA  # replace from
setD = setB - setA  # replace to

print(len(setJ), len(setA), len(setB), len(setC), len(setD))

if len(setC) < len(setD):
    # 使用了太多 CP932 中不存在的字母，无法完成替换
    raise Exception('too much replacements, try reducing chars in NEW text')

alt_encoding = {}
exec_writes = []

for replace_fr, replace_to in zip(setC, setD):
    if ord(replace_to) > 0xFFFF:
        # 使用的 Unicode 字母的编码超出了两个字节能够表示的范围
        raise Exception('unicode out of u16 range')

    data_jis = replace_fr.encode('cp932')
    data_u16 = replace_to.encode('utf-16le')
    code_jis = U16_BE.unpack(data_jis)[0]
    code_u16 = U16_LE.unpack(data_u16)[0]
    file_off = offJ[code_jis]

    alt_encoding[replace_to] = data_jis
    exec_writes.append((file_off, data_u16))


with open(OROOT + 'main', 'wb') as fp:
    with open(FPATH_MAIN, 'rb') as fi:
        data = bytearray(fi.read())
    for file_off, data_u16 in exec_writes:
        data[file_off:file_off+2] = data_u16
    fp.write(data)


for fname in FNAME:
    with open(NROOT + fname + '.json', 'r') as fp:
        s_pairs = json.load(fp)
    with open(FROOT + fname, 'rb') as fp:
        assert fp.read(16) == MAGIC
        ins_len, str_len, off_len = U32_3.unpack(fp.read(16)[0:12])
        assert off_len % 4 == 0
        ins_data = fp.read(ins_len)
    if off_len / 4 != len(s_pairs):
        # 与原文件中字符串数量不一致
        raise Exception('string count does not match original')
    str_data = bytearray()
    off_data = bytearray()
    knownstr = dict()
    for s_pair in s_pairs:
        s_new = s_pair['new']
        if s_new in knownstr:
            off_data.extend(knownstr[s_new])
        else:
            new_off = knownstr[s_new] = U32_LE1.pack(len(str_data))
            off_data.extend(new_off)
            for ch in s_new:
                if ch in alt_encoding:
                    str_data.extend(alt_encoding[ch])
                else:
                    str_data.extend(ch.encode('cp932'))
            str_data.append(0)
            while len(str_data) % 16 != 0:
                str_data.append(0)
    with open(OROOT + fname, 'wb') as fp:
        fp.write(MAGIC)
        fp.write(U32_3.pack(ins_len, len(str_data), len(off_data)))
        fp.write(bytes([0, 0, 0, 0]))
        fp.write(ins_data)
        fp.write(str_data)
        fp.write(off_data)
