# Dotfiles

Hyprland, Ghostty, Omarchy bar, and default-terminal configs, managed with Git + GNU Stow.
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
stow --target="$HOME" --no-folding hypr ghostty omarchy terminal
```

Omarchy updates/resets can overwrite configs or replace links. Review changes afterward.
Backed up to the private GitHub repo `fotisk07/dotfiles`. Run `git push` after committing.
