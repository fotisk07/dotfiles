# Dotfiles

Hyprland, Ghostty, Omarchy bar, three personal art palettes, and default-terminal configs, managed with Git + GNU Stow.

Personal palettes: **Willow** (daily driver), **Lagoon**, and **Sylvan**. See [the theme guide](docs/themes.md) for palette locations, verified artwork downloads, installation, and the macOS portability plan.
Edit normally in `~/.config/`; symlinks point here.

## Save changes

```bash
cd ~/dotfiles
git diff
git add -p
git commit -m "Describe changes"
```

## Install

Back up and move aside existing configs first. Review monitor settings on a new machine.

```bash
cd ~/dotfiles
python3 scripts/theme-wallpapers.py --link-omarchy
stow --target="$HOME" --no-folding hypr ghostty terminal
stow --target="$HOME" omarchy
```

Use normal directory folding for `omarchy` so each custom theme is linked as a folder; do not use `--no-folding` for that package. Existing theme directories must be backed up and moved aside first. Stow does not activate a theme; choose one explicitly, e.g. `omarchy theme set willow`.

Omarchy updates/resets can overwrite configs or replace links. Review changes afterward.
Backed up to the private GitHub repo `fotisk07/dotfiles`. Run `git push` after committing.
