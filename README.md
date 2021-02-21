# tmux-starter

A little script to setup your tmux session. 

## Installation

``` shell
git clone git@github.com:Bergschrat1/tmux-starter.git && cd tmux-starter
pip install .
```

## Usage
Create a file `session_data.json` at `~/.config/pymux/session_data.json`. You can also place the configuration at a path that you can specify with the `--config` option when calling the script.

Have a look at session_data.json.example to get idea of how to configure your config file.

`session_data.json` is a list of dictionaries. Each dictionary represents a tmux session and has the keys `name`, `windows` and `default`.

- `name` is the name of the session
- `windows` is a list of dictonaries which, where each dictionary represents a window.
- `default` is a boolean value and determines if this session is created when running the script without extra arguments (for startup)

For the window setup you can give the keys `name`, `panes` and `commands` to each dictionary.
- `name` is the name of the window.
- `panes` is an integer which determines the number of panes on that window.
- `commands` is a list of strings. Each string represents a command that will be executed in the respective pane. If you want an empty pane you can just insert an empty string ("").
