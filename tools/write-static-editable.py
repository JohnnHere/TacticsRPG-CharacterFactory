"""Lossless one-frame RGBA ASE source, without inventing separated outfit layers."""
import argparse
import struct
import zlib
from pathlib import Path
from PIL import Image

def chunk(kind,data):
    return struct.pack('<IH',len(data)+6,kind)+data

def write_static(source,target,label):
    image=Image.open(source).convert('RGBA')
    if image.size!=(128,128):raise ValueError('Native 128x128 canvas required')
    name=label.encode('utf-8')
    layer=struct.pack('<6HB3xH',3,0,0,0,0,0,255,len(name))+name
    cel=struct.pack('<HhhBHh5xHH',0,0,0,255,2,0,128,128)+zlib.compress(image.tobytes(),9)
    payload=chunk(0x2004,layer)+chunk(0x2005,cel)
    frame=struct.pack('<IHHH2xI',len(payload)+16,0xF1FA,2,100,0)+payload
    header=bytearray(128)
    struct.pack_into('<I5HIH',header,0,128+len(frame),0xA5E0,1,128,128,32,1,100)
    header[34:36]=b'\x01\x01'
    struct.pack_into('<HH',header,40,16,16)
    Path(target).write_bytes(header+frame)
    print(f'{target}: 1 frame, full-body RGBA raster, no clothing rig')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('target');ap.add_argument('--label',default='Body and outfit - weaponless')
    a=ap.parse_args();write_static(a.source,a.target,a.label)
