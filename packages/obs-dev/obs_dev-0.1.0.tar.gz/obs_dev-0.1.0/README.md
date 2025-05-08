# obs-dev
A command-line tool for Obsidian development, helping with vault management and plugin development.
(allows live sync of plugins to test vaults)

## Installation

```bash
# Install using pip
pip install obs-dev

```

## Command Structure

```
obs-dev
├── plugin - Manage Obsidian plugins
│   ├── build    - Build the plugin
│   ├── create   - Create a new plugin
│   ├── install  - Install the plugin to a vault
│   ├── repair   - Repair plugin configs
│   ├── test     - Test the plugin
│   └── watch    - Watch for changes and rebuild
│
└── vault - Manage Obsidian vaults
    ├── btoggle  - Batch toggle multiple vaults
    ├── create   - Create a new vault
    ├── list     - List registered vaults
    ├── open     - Open a vault
    ├── unregister - Unregister a vault
    └── toggle   - Toggle vault state
```

## Features

### Vault Management

- Create new Obsidian vaults
- Open, toggle, and manage existing vaults
- List registered vaults
- Batch operations on multiple vaults

### Plugin Development

- Create new plugin projects with boilerplate code
- Build plugins with version control
- Install plugins to vaults
- Test plugins in target vaults
- Watch for changes and automatically rebuild
- Repair plugin configurations

## Usage

### Running with Rye

If using Rye as your package manager:

```bash
rye run obs-dev [command] [options]
```

### Vault Commands

```bash
# Create a new vault
obs-dev vault create /path/to/vault --open

# Open a vault by id, path or name
obs-dev vault open --id <vault-id>
obs-dev vault open --path /path/to/vault
obs-dev vault open --name VaultName

# Toggle vault state
obs-dev vault toggle --name VaultName --state open
obs-dev vault toggle --name VaultName --state closed

# Batch toggle multiple vaults
obs-dev vault btoggle --toggle "id(xxx)=1" --toggle "name(yyy)=0"
obs-dev vault btoggle --off-all

# List registered vaults
obs-dev vault list
```

### Plugin Commands

```bash
# Create a new plugin
obs-dev plugin create --path /path/to/plugin --name "My Plugin" --description "Plugin description" --author "Your Name"

# Repair plugin configuration
obs-dev plugin repair --path /path/to/plugin

# Build a plugin
obs-dev plugin build --path /path/to/plugin --ver-increment patch

# Install a plugin to a vault
obs-dev plugin install --path /path/to/plugin --vault VaultName --open

# Test a plugin in a vault
obs-dev plugin test --path /path/to/plugin --target VaultName

# Watch for changes and automatically rebuild
obs-dev plugin watch --path /path/to/plugin --target VaultName --src-only
```

## Dependencies

Required:
- click >= 8.1.8
- packaging >= 25.0

Optional:
- watchdog >= 3.0.0 (for watch functionality)

## Development

This project uses [Rye](https://rye-up.com/) for Python package management. To contribute:

```bash
# Clone the repository
git clone https://github.com/ZackaryW/obs-dev.git
cd obs-dev

# Install dependencies with Rye
rye sync

# Run the tool
rye run obs-dev
```
