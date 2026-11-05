#!/usr/bin/env python3
"""Build the copy of Crownhold that is published as a Claude Artifact.

The artifact host serves only standard web types, so it cannot serve .glb or .hdr.
This writes dist/artifact/ with index.html switched to ASSET_WRAPPED = true and the
models / skies wrapped as base64 JSON (*.glb.json is a plain glTF with an embedded
buffer, *.hdr.json is {"format": "radiance-hdr", "b64": ...}). Everything else is
published from the repo as is.

Usage: python3 tools/build-artifact.py
"""
import base64, glob, json, os, struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'dist', 'artifact')


def glb_to_gltf_json(data):
    magic, version, _ = struct.unpack_from('<4sII', data, 0)
    assert magic == b'glTF' and version == 2
    off, js, binb = 12, None, b''
    while off < len(data):
        n, kind = struct.unpack_from('<I4s', data, off)
        chunk = data[off + 8:off + 8 + n]
        if kind == b'JSON': js = json.loads(chunk)
        elif kind == b'BIN\0': binb = chunk
        off += 8 + n
    js['buffers'][0]['uri'] = 'data:application/octet-stream;base64,' + base64.b64encode(binb[:js['buffers'][0]['byteLength']]).decode()
    return json.dumps(js, separators=(',', ':'))


def main():
    os.makedirs(os.path.join(OUT, 'assets', 'models'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'assets', 'hdri'), exist_ok=True)
    html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    assert html.count('const ASSET_WRAPPED = false;') == 1
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html.replace('const ASSET_WRAPPED = false;', 'const ASSET_WRAPPED = true;'))
    for f in glob.glob(os.path.join(ROOT, 'assets', 'models', '*.glb')):
        open(os.path.join(OUT, 'assets', 'models', os.path.basename(f) + '.json'), 'w').write(glb_to_gltf_json(open(f, 'rb').read()))
    for f in glob.glob(os.path.join(ROOT, 'assets', 'hdri', '*.hdr')):
        b64 = base64.b64encode(open(f, 'rb').read()).decode()
        open(os.path.join(OUT, 'assets', 'hdri', os.path.basename(f) + '.json'), 'w').write(json.dumps({'format': 'radiance-hdr', 'b64': b64}))
    print('wrote', OUT)


if __name__ == '__main__':
    main()
