<div align="center">
  <img src=".readme/logo.png" alt="FASCI CLI" width="360"><br><br>
</div>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Install](https://img.shields.io/badge/install-curl%20%7C%20bash-3775a9.svg)](#installation)
[![Status](https://img.shields.io/badge/status-active-success.svg)](#)

-----------------

**FASCI CLI** is the command-line client for FASCI — the verifiable civic-engagement platform for organizing campaigns, events, protests, and boycotts. It lets you manage campaigns, boosts, and subscriptions directly from your terminal, talking to the FASCI API.

Use it to list and inspect campaigns, create and cancel boosts, check your subscription and portfolio metrics, and diagnose connectivity — all scriptable, with JSON output for automation. It authenticates with a `FASCI_API_KEY` against the hosted FASCI API (or a local backend during development).

## Installation

```bash
curl -fsSL https://downloads.fasci.app/cli/install.sh | bash
```

From source (a clone of this repo):

```bash
pip install -e .
```

`fasci-cli` is not published on PyPI; use the installer above or a source install.

Standalone binary:

```bash
./install.sh --version <version>
```

Environment:
- `FASCI_DOWNLOADS_BASE_URL` (default: `https://downloads.fasci.app`)
- `FASCI_NO_UPDATE_CHECK=1` to disable update checks

## Authentication

Authenticate interactively, or set an API key. Config is stored at `~/.fasci/config.yaml`:

```yaml
api_key: your-api-key
api_url: https://api.fasci.app
```

Or via environment variables:

```bash
export FASCI_API_KEY=your-api-key
export FASCI_API_URL=https://api.fasci.app   # or http://localhost:8001 for local dev
```

```bash
fasci login       # authenticate with FASCI
```

## Quick Start

```bash
fasci login                    # Authenticate
fasci campaigns list           # List campaigns
fasci boosts list              # List boosts
fasci subscriptions me         # Check your subscription
fasci status                   # System status
```

## Commands

| Command | Description |
|---|---|
| `fasci login` | Authenticate with FASCI |
| `fasci campaigns list` | List campaigns |
| `fasci campaigns get <id>` | Get campaign details |
| `fasci campaigns delete <id>` | Delete a campaign |
| `fasci boosts list` | List boosts |
| `fasci boosts get <id>` | Get boost details |
| `fasci boosts create` | Create a new boost |
| `fasci boosts cancel <id>` | Cancel a boost |
| `fasci subscriptions tiers` | List subscription tiers |
| `fasci subscriptions me` | View your subscription |
| `fasci metrics portfolio` | View portfolio metrics |
| `fasci status` | Show system status |
| `fasci doctor` | Diagnose connection issues |
| `fasci completion bash` | Generate shell completion |

## Output formats

```bash
fasci campaigns list --output json    # JSON output (for scripting)
fasci campaigns list --quiet          # IDs only
```

## Stack

- Python 3.9+ · `click` (CLI) · `httpx` (HTTP) · `rich` (terminal rendering)

## Documentation & resources

- **Project overview**: ../README.md
- **CLI user guide**: ../docs/CLI_USER_GUIDE.md · command reference
- **API reference**: ../docs/API_REFERENCE.md
- **Hosted API**: `https://api.fasci.app` · **Product site**: `https://fasci.app`

## License

This project is licensed under the MIT License.
