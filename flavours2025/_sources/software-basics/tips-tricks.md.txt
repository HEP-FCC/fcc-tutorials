# Tips and tricks

## Autocompletion using bash history

Add

```
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'
```

to the file `$HOME/.bashrc` to cycle through previously executed command with the up/down keys.
