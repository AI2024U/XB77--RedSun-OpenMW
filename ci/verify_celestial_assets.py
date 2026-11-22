#!/usr/bin/env python3
"""Verify XB77 Celestial A resources in a portable ZIP or extracted folder.

Usage: python ci/verify_celestial_assets.py "XB77 Red Sun OpenMW.zip"
This checks assets only; it does NOT prove that the native engine animates.
"""
from __future__ import annotations

import hashlib
import struct
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

PREFIX = 'resources/vfs/'
STATIC = PREFIX + 'textures/omw_steam_button_a.dds'
LAYOUT = PREFIX + 'mygui/openmw_controllerbuttons.layout'
FRAMES = [PREFIX + f'textures/xb77_celestial_a_{i:02}.png' for i in range(12)]


def png_info(data: bytes) -> tuple[int, int, int]:
    if len(data) < 29 or data[:8] != b'\x89PNG\r\n\x1a\n' or data[12:16] != b'IHDR':
        raise ValueError('Not a valid PNG header')
    width, height = struct.unpack('>II', data[16:24])
    return width, height, data[25]


def verify_asset(read):
    texture = read(STATIC)
    if len(texture) < 128 or texture[:4] != b'DDS ':
        raise ValueError('A texture does not have a DDS header')
    h, w = struct.unpack_from('<II', texture, 12)
    if (w, h) != (256, 256):
        raise ValueError(f'Expected a 256x256 static A texture, found {w}x{h}')
    if texture[84:88] != b'DXT5':
        raise ValueError('Expected the compatible DXT5 (BC3) texture format')

    layout = ET.fromstring(read(LAYOUT))
    widgets = [e for e in layout.iter('Widget') if e.get('name') == 'BtnAImage']
    if len(widgets) != 1:
        raise ValueError(f'Expected one BtnAImage, found {len(widgets)}')
    button = widgets[0]
    props = {p.get('key'): p.get('value') for p in button.findall('Property')}
    if props.get('ImageTexture', '').replace('\\', '/') != 'textures/omw_steam_button_a.dds':
        raise ValueError('Controller A texture reference does not match')
    if props.get('Colour', '').lower() not in {'#ffffff', '#fff'} or float(props.get('Alpha', '0')) != 1.0:
        raise ValueError('A prompt is tinted or not fully opaque')
    size = button.get('position', '').split()
    if len(size) != 4 or size[2:] != ['28', '28']:
        raise ValueError('Expected the reviewed 28px A prompt size')

    for idx, name in enumerate(FRAMES):
        data = read(name)
        width, height, colour = png_info(data)
        if (width, height) != (256, 256) or colour != 6:
            raise ValueError(f'Unexpected PNG geometry or color type for frame {idx}: {width}x{height}, {colour}')

    print('PASS: static 256x256 DXT5 A texture, untinted 28px layout, all 12 RGBA frames')
    print('Static A texture SHA256:', hashlib.sha256(texture).hexdigest())
    print('NOTE: The build requires a separately compiled native engine with the animation source patch.')


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: verify_celestial_assets.py <portable-zip-or-extracted-folder>')
    path = Path(sys.argv[1])
    if path.is_file():
        with zipfile.ZipFile(path) as z:
            required = {STATIC, LAYOUT, *FRAMES}
            missing = sorted(required - set(z.namelist()))
            if missing:
                raise ValueError(f'Missing resources in ZIP: {missing}')
            verify_asset(z.read)
    elif path.is_dir():
        verify_asset(lambda relative: (path / relative).read_bytes())
    else:
        raise SystemExit(f'Path not found: {path}')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        raise SystemExit(f'FAIL: {exc}') from exc
