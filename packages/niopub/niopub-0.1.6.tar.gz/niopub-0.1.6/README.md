# Niopub CLI

For creating and managing context-based agents, available on the Niopub app, from your browser.

## Installation

You can install Niopub CLI using pip:

```bash
pip install niopub
```

Or install from a local clone:

```bash
git clone https://github.com/Niopub/niopub.git
cd niopub
pip install .
```

## Usage

After installation, you can start the Niopub server with a simple command:

```bash
niopub
```

This will start the server on the default port 8000. You can also specify a custom port:

```bash
niopub 8080
```

You can then access the Niopub interface by opening your browser to:

```
http://localhost:8000
```

### Features

- Create and manage context-based agents
- Monitor agent processes
- Pause, resume, and stop agents
- Web-based interface for easy management

### Requirements

- Python 3.8 or higher
- Dependencies will be automatically installed with pip

## Development

To install in development mode:

```bash
git clone https://github.com/Niopub/niopub.git
cd niopub
pip install -e .
```

## License

MIT License - See LICENSE file for details
