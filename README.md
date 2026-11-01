# Dotfiles

Hyprland and Ghostty configs, managed with Git + GNU Stow.
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
stow --target="$HOME" --no-folding hypr ghostty
```

Omarchy updates/resets can overwrite configs or replace links. Review changes afterward.
Local repo only; no remote backup configured.
