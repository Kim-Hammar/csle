# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CSLE (Cyber Security Learning Environment) is a platform for evaluating and developing reinforcement learning agents for control problems in cyber security. It consists of three main systems:

- **Simulation System** (`simulation-system/`): RL algorithms, Markov games, and gym environments (Python)
- **Emulation System** (`emulation-system/`): Docker-based infrastructure emulation for realistic cyber environments
- **Management System** (`management-system/`): Web UI (React), REST API, and monitoring (Prometheus/Grafana)

## Common Commands

### Running Tests

```bash
# All unit tests (Python + JavaScript)
./unit_tests.sh

# Single Python library tests
cd simulation-system/libs/csle-common && pytest
cd simulation-system/libs/csle-agents && pytest --cov=csle_agents

# JavaScript tests
cd management-system/csle-mgmt-webapp && npm test
```

### Linting

```bash
# All linting (Python + JavaScript)
./linter.sh

# Python only
flake8 simulation-system/
flake8 emulation-system/envs

# JavaScript only
cd management-system/csle-mgmt-webapp && npx eslint . --quiet
```

### Type Checking

```bash
# All Python type checking
./type_checker.sh

# Single library
cd simulation-system/libs/csle-common && mypy src tests
```

### Building and Installing Python Libraries

Each library in `simulation-system/libs/` has a Makefile:

```bash
cd simulation-system/libs/csle-common
make install_dev  # Install dev dependencies
make install      # Install package in editable mode (pip install -e .)
make unit_tests   # Run pytest with coverage
make lint         # Run flake8
make types        # Run mypy
make docs         # Build Sphinx documentation
```

### Web Application

```bash
cd management-system/csle-mgmt-webapp
npm install
npm run dev       # Development server (port 3005)
npm run build     # Production build
npm run lint      # ESLint
npm run format    # Prettier formatting
```

## Architecture

### Python Library Dependency Layers

```
Layer 1 (Foundation):  csle-base (no CSLE dependencies)
Layer 2 (Core):        csle-common, csle-collector, csle-ryu
Layer 3 (Actions):     csle-attacker, csle-defender
Layer 4 (Algorithms):  csle-agents, csle-system-identification
Layer 5 (Integration): csle-rest-api, csle-cli, csle-cluster
Layer 6 (Environments): gym-csle-stopping-game, gym-csle-apt-game,
                        gym-csle-intrusion-response-game, gym-csle-cyborg
```

### Python Package Structure

All libraries use src layout with modern Python packaging:

```
csle-{name}/
├── pyproject.toml     # Package metadata and build config
├── setup.py           # Minimal (delegates to pyproject.toml)
├── requirements.txt   # Runtime dependencies
├── requirements_dev.txt
├── src/csle_{name}/   # Source code
└── tests/             # pytest tests
```

### Key Technologies

- **Python**: gymnasium, torch, stable-baselines3, grpcio, docker, psycopg
- **JavaScript**: React 18, Vite, React Router 6, xterm.js, recharts, socket.io-client
- **Infrastructure**: Docker, PostgreSQL (Citus), Prometheus, Grafana, Open vSwitch

### Shared Database (Metastore)

All systems share a PostgreSQL database. Schema is in `metastore/`:
- `create_db.sql` - Database initialization
- `create_tables.sql` - Table definitions

## Code Style

### Python
- PEP 8 with flake8 (max line length: 120)
- snake_case for functions and variables
- Type hints required (mypy strict mode)
- All functions/classes need docstrings with `:param` and `:return:`

### JavaScript
- ESLint + Prettier
- CamelCase for functions and variables
- ES modules (type: "module")

## Git Workflow

Uses Git-Flow branching:
- `master` - Stable releases
- `develop` - Integration branch
- `feature/*` - New features
- `hotfix/*` - Critical fixes

PRs must pass CI (GitHub Actions) before merge. Tests are required for new features.
