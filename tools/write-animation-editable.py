"""Write lossless RGBA animation sources in the documented ASE format.

No drawing/deformation occurs. Each source cel stores exactly the native PNG.
Validated by exporting from LibreSprite and comparing every RGBA pixel.
Format: https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md
"""
import argparse
import json
import struct
import zlib
from pathlib import Path
from PIL import Image


def chunk(kind, data):
    return struct.pack("<IH", len(data)+6, kind)+data


def write_clip(folder):
    folder=Path(folder)
    clip=json.loads((folder/"clip.json").read_text(encoding="utf-8"))
    state,direction,count=clip["state"],clip["direction"],clip["frames"]
    duration=clip["durationMs"]
    frames=[]
    for i in range(count):
        image=Image.open(folder/f"{state.lower()}_{direction}_{i:02d}.png").convert("RGBA")
        if image.size!=(128,128): raise ValueError("Native canvas required")
        chunks=[]
        if i==0:
            name=clip.get("layerName","Body and Warrior outfit - weaponless").encode('utf-8')
            layer=struct.pack("<6HB3xH",3,0,0,0,0,0,255,len(name))+name
            chunks.append(chunk(0x2004,layer))
        cel=struct.pack("<HhhBHh5xHH",0,0,0,255,2,0,128,128)+zlib.compress(image.tobytes(),9)
        chunks.append(chunk(0x2005,cel))
        payload=b"".join(chunks)
        frames.append(struct.pack("<IHHH2xI",len(payload)+16,0xF1FA,len(chunks),duration,0)+payload)
    payload=b"".join(frames)
    header=bytearray(128)
    struct.pack_into("<I5HIH",header,0,128+len(payload),0xA5E0,count,128,128,32,1,duration)
    header[34:36]=b"\x01\x01"
    struct.pack_into("<HH",header,40,16,16)
    target=folder/f"{state.lower()}_{direction}.aseprite"
    target.write_bytes(header+payload)
    print(f"{target}: {count} native editable cels, {duration} ms/frame")


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("folder")
    write_clip(ap.parse_args().folder)
