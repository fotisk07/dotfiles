# Personal dotfiles

Omarchy user configuration managed with Git and GNU Stow. Edit the usual files
under `~/.config/`: they are file-level symlinks into this repository.

## Packages

- `hypr`: Hyprland user configuration, monitor layout, and night light
- `ghostty`: terminal preferences and keyboard bindings

Alacritty and Kitty configs remain ordinary files outside this repository.

Generated Omarchy theme files, caches, backups, and credentials are not managed.
Bash, tmux, Neovim, and the Omarchy bar are not included yet.

## Everyday use

```bash
cd ~/dotfiles
git status
git diff
# Review changes before saving them:
git add -p
git commit -m "Describe the configuration change"
```

Git does not save commits automatically. This is a local repository; a remote
backup has not been configured.

## Install links

Install GNU Stow, clone this repo to `~/dotfiles`, then:

```bash
cd ~/dotfiles
stow --target="$HOME" --no-folding --simulate hypr ghostty
stow --target="$HOME" --no-folding hypr ghostty
```

Existing regular config files cause conflicts. Back them up and move them out of
the way first. Do not use `--adopt` blindly: it moves existing live files into the
repository and can replace the repository's saved versions.

Use `--no-folding` so only individual files are linked; config directories remain
ordinary directories and can still hold unmanaged files.

The monitor layout is machine-specific: review `hypr/.config/hypr/monitors.lua`
before applying it on another computer.

## Omarchy updates and resets

The installed `omarchy refresh config` implementation uses `cp -f`, which writes
through these file symlinks. A reset can therefore overwrite the working-tree
version of a managed config; committed versions remain in Git history. Other
updates or migrations may replace symlinks instead, so inspect links and Git
changes after updating. Do not reset configs expecting Stow to protect contents.

If a link is replaced by a regular file, compare it with the repository before
backing it up, moving it aside, and restowing the relevant package.

To remove managed links without deleting the repository:

```bash
cd ~/dotfiles
stow --target="$HOME" --no-folding --delete hypr ghostty
```

This removes the live config paths; restore ordinary copies if you are retiring
Stow rather than temporarily unlinking packages.

## Initial backup

Original files and their SHA-256 manifest were saved outside the repository at:

`~/.local/state/dotfiles-backups/20261101-220428/`

All 12 live config files were verified byte-for-byte unchanged after linking.
