#!/usr/bin/env python3
"""Fetch verified originals and render wallpapers. Does not activate any theme."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import urllib.request

REPO = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fetch(art, original, offline):
    if original.exists():
        if digest(original) != art['sha256']:
            raise ValueError(f'Cached original failed checksum verification: {original}')
        return
    if offline:
        raise FileNotFoundError(f'Original not cached: {original}')
    request = urllib.request.Request(art['download_url'], headers={
        'User-Agent': 'PersonalDotfilesArtThemes/1.0 (personal desktop wallpapers)',
    })
    original.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=original.parent, delete=False) as stream:
            temporary = Path(stream.name)
            with urllib.request.urlopen(request, timeout=120) as response:
                shutil.copyfileobj(response, stream)
        if digest(temporary) != art['sha256']:
            raise ValueError(f'Download checksum mismatch; refusing image: {art["title"]}')
        temporary.replace(original)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def render(original, destination, size, gravity):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix='.png', delete=False) as stream:
            temporary = Path(stream.name)
        subprocess.run(['magick', str(original), '-auto-orient', '-resize', size + '^',
                        '-gravity', gravity, '-extent', size, str(temporary)], check=True)
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('themes', nargs='*', help='Default: willow lagoon sylvan')
    parser.add_argument('--offline', action='store_true', help='Use only verified cached originals')
    parser.add_argument('--cache-dir', type=Path, help='Default: <output-dir>/.originals')
    parser.add_argument('--output-dir', type=Path, default=Path.home() / '50_Media/Wallpapers/Omarchy',
                        help='Media destination; default: ~/50_Media/Wallpapers/Omarchy')
    parser.add_argument('--link-omarchy', action='store_true',
                        help='Link generated artwork into the repository theme folders (no image copies)')
    args = parser.parse_args()
    args.output_dir = args.output_dir.expanduser().resolve()
    args.cache_dir = (args.cache_dir or args.output_dir / '.originals').expanduser().resolve()
    manifest = json.loads((REPO / 'theme-assets.json').read_text())
    themes = args.themes or list(manifest['themes'])
    unknown = set(themes) - manifest['themes'].keys()
    if unknown:
        parser.error('Unknown themes: ' + ', '.join(sorted(unknown)))
    if not shutil.which('magick'):
        parser.error('ImageMagick 7 is required (magick command)')
    for slug in themes:
        art = manifest['themes'][slug]
        original = args.cache_dir / slug / 'original.jpg'
        fetch(art, original, args.offline)
        dimensions = subprocess.check_output(['magick', 'identify', '-format', '%w %h', str(original)], text=True)
        expected = f'{art["original_width"]} {art["original_height"]}'
        if dimensions != expected:
            raise ValueError(f'Unexpected dimensions for {slug}: {dimensions}, expected {expected}')
        # All approved sources are large enough: neither crop dimension is upscaled.
        width, height = map(int, manifest['wallpaper_size'].split('x'))
        if art['original_width'] < width or art['original_height'] < height:
            raise ValueError(f'{slug}: original too small; refusing to upscale')
        folder = args.output_dir / slug
        (folder / 'backgrounds').mkdir(parents=True, exist_ok=True)
        wallpaper = folder / 'backgrounds/01-fullbleed.png'
        render(original, wallpaper, manifest['wallpaper_size'], art['crop_gravity'])
        render(wallpaper, folder / 'preview.png', manifest['preview_size'], 'center')
        if args.link_omarchy:
            theme = REPO / 'omarchy/.config/omarchy/themes' / slug
            if not (theme / 'colors.toml').is_file():
                raise FileNotFoundError(f'Missing palette: {theme}')
            for name in ['backgrounds', 'preview.png']:
                link, target = theme / name, folder / name
                if link.is_symlink() and link.resolve() == target:
                    continue
                if link.exists() or link.is_symlink():
                    raise FileExistsError(f'Move existing artwork aside before linking: {link}')
                link.symlink_to(target, target_is_directory=name == 'backgrounds')
        print(f'{slug}: {wallpaper}')


if __name__ == '__main__':
    main()
