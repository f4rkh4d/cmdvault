# cmdvault

Save, search, and run your terminal commands from a personal vault.

Stop googling the same `docker compose` flags or scrolling through shell history. Save commands once, find them instantly.

## Install

```bash
pip install cmdvault
```

## Usage

### Save a command

```bash
cmdvault add "docker compose -f dev.yml up --build" -d "Start dev environment" -t docker,dev
```

### Find commands

```bash
cmdvault find docker
```

```
┌──────────┬──────────────────────────────────────┬───────────────────────┬────────────┐
│ ID       │ Command                              │ Description           │ Tags       │
├──────────┼──────────────────────────────────────┼───────────────────────┼────────────┤
│ a1b2c3d4 │ docker compose -f dev.yml up --build │ Start dev environment │ docker,dev │
└──────────┴──────────────────────────────────────┴───────────────────────┴────────────┘
```

### Run a command

```bash
cmdvault run a1b2c3d4
```

### Placeholders

Save commands with variables. cmdvault will ask for values at runtime:

```bash
cmdvault add "ssh {{user}}@{{host}}" -d "SSH to server" -t ssh
cmdvault run a1b2c3d4
#   user: root
#   host: 10.0.0.1
# → ssh root@10.0.0.1
```

### All commands

| Command | Description |
|---------|-------------|
| `cmdvault add <cmd>` | Save a command (`-d` description, `-t` tags) |
| `cmdvault list` | Show all saved commands |
| `cmdvault find <query>` | Fuzzy search by keyword, tag, or text |
| `cmdvault run <id>` | Execute a saved command |
| `cmdvault edit <id>` | Edit a command (`-c`, `-d`, `-t`) |
| `cmdvault rm <id>` | Remove a command |
| `cmdvault export` | Export vault as JSON |
| `cmdvault import <file>` | Import commands from JSON file |

### Options

- `--dry-run` on `run`. print the command without executing
- `-y` on `rm`. skip confirmation

## Data

Commands are stored in `~/.cmdvault.json`. Back up with `cmdvault export > backup.json`.

## License

MIT
