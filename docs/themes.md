# Personal art palettes

## The approved set

| Palette | Character | Painting | Main background |
|---|---|---|---|
| Willow | Calm blue-grey with sage, sky blue and lavender; daily-driver choice | Monet, The Water-Lily Pond | `#30383A` |
| Lagoon | Deep slate blue, powder blue, lagoon green and sandstone | Canaletto, The Entrance to the Grand Canal, Venice | `#242F3D` |
| Sylvan | Original dark slate, sage, dusty rose and champagne | Fragonard, The Progress of Love: The Lover Crowned | `#293137` |

These are the approved palettes after fixing the external display settings. Sylvan's original palette was restored; intermediate brighter/greener/lavender variants and Reverie are not part of this collection.

## What is the source of truth?

Each palette lives once:

```
omarchy/.config/omarchy/themes/<name>/colors.toml
```

This is plain color data, not a Linux-only application. Background/text shades, selection colors, accents and ANSI colors are named there. The locations are convenient for Stow and Omarchy; macOS tools can read the same TOML files.

Omarchy generates app-specific configuration through its built-in templates when applying a palette. There are no hand-maintained copies of the palette in VS Code, terminal or Neovim files in this repository. The original creation scripts and their comments are historical, not required for installation. Edit the TOML files here instead.

The rendering templates belong to the installed Omarchy version: a future version can map the same colors differently. If exact cross-platform app rendering is needed, add a versioned exporter later rather than creating manually edited color duplicates.

## Artwork is separate

`theme-assets.json` records each painting's source, source credit, original dimensions, SHA-256 checksum and crop. Originals and rendered PNGs are not committed to Git.

Wallpapers fill the screen, without margins, stretching or color modifications. ImageMagick crops each original to 2560×1600. Willow and Lagoon use center crops; Sylvan uses a bottom-aligned crop to retain the couple. A 16:9 display can crop a little more vertically when filling its screen. All originals are larger than the rendered wallpaper: no upscaling is needed.

The source paintings are recorded as public domain on Commons. Source provenance and the terms of a particular reproduction should still be checked before redistribution. Willow's record cites multiple sources; do not describe it as an exclusively direct museum download.

### Download and generate

Requirements: Python 3.11+ and ImageMagick 7 (`magick`). The Python script has no third-party package dependencies.

From the repository root:

```bash
python3 scripts/theme-wallpapers.py --link-omarchy
```

All generated images live under `~/50_Media/Wallpapers/Omarchy/`, with originals cached in its `.originals/` subdirectory. `--output-dir` can select a different media location. Downloads are verified against the recorded hashes before use. A changed or corrupt image is rejected rather than silently accepted. `--link-omarchy` adds Git-ignored artwork symlinks to the repository theme folders; no image copies are kept in dotfiles.

To build just one palette's artwork:

```bash
python3 scripts/theme-wallpapers.py willow
```

To rebuild from the cache without internet access:

```bash
python3 scripts/theme-wallpapers.py --offline
```

The script fetches/renders artwork and, with `--link-omarchy`, creates artwork links. It does not apply themes, change app preferences, or install packages. It overwrites only its named generated wallpaper/preview outputs. User-added wallpaper files are left alone. It refuses to replace existing files/directories with links; move those aside first if migrating an older layout.

## Install on another Omarchy computer

1. Clone this dotfiles repository and install the requirements above.
2. Generate the artwork using the script.
3. Back up existing configurations. If theme directories with these names already exist, move them outside `~/.config/omarchy/themes/` first so they cannot conflict with Stow.
4. Preview and apply Stow:

```bash
cd ~/dotfiles
stow --simulate --verbose --target="$HOME" omarchy
stow --target="$HOME" omarchy
```

**Allow normal Stow directory folding for the `omarchy` package.** The three theme directories should be directory symlinks. Do not apply `--no-folding` to this package: palette-file symlinks inside real theme directories can become broken relative links when Omarchy copies files to its staging directory.

Omarchy also includes the existing shell configuration in this package. Review that package's other files before installing it on a different machine.

Applying a theme is a separate, explicit action:

```bash
omarchy theme set willow
omarchy theme set lagoon
omarchy theme set sylvan
```

Theme changes affect supported applications, not only wallpaper. VS Code normally selects Omarchy's generated local theme; Neovim uses Omarchy's Aether integration. First-time installation or changed app versions may need an editor reload. No automatic time-based switching is configured. Willow is the preferred daily driver, not forcibly selected during installation.

## macOS / work computer

Do **not** Stow the Linux `hypr` or `omarchy` packages onto a Mac. The portable pieces are the same three TOML palettes plus the painting/crop metadata.

Mac app exports are **not implemented yet**. The next portability step is a generator that reads these same palettes and produces:

- standalone Ghostty color files;
- a local VS Code theme extension with all three choices;
- a Neovim theme configuration without Omarchy state paths.

That should change only theme selection, not replace complete work-machine app configs. Check workplace policy before cloning personal dotfiles or downloading/installing themes. Art generation itself can run on macOS with Python 3.11+ and ImageMagick:

```bash
python3 scripts/theme-wallpapers.py --output-dir "/path/to/your/media/Art Themes"
```

## Display lesson

Screenshots show rendered pixels, not the physical panel's contrast, gamma, brightness, overscan or picture mode. Resetting/fixing the external display made its colors much closer to the laptop. Check display settings before compensating through palette changes. The approved set should not include accidental monitor-specific color compensation.

## Saving changes

Edit the canonical TOML through the linked theme folder or directly here, apply that theme to preview, then review Git's diff. Generated artwork is ignored.

```bash
git diff
git status --short
```

Committing and pushing are deliberate steps; Stow does neither. Keep rejected experiments, private screenshots and local backups outside Git.
