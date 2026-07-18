# fasci CLI

CLI tool for fasci campaign management — manage campaigns, boosts, and subscriptions from your terminal.

## Installation

```bash
pip install fasci-cli
```

Or from source:
```bash
cd /Users/latarencebutts/ahl/fasci/cli
pip install -e .
```

### Install Standalone Binary

```bash
./install.sh --version <version>
```

Environment:
- `FASCI_DOWNLOADS_BASE_URL` (default: `https://downloads.fasci.app`)

Disable update checks:
- `FASCI_NO_UPDATE_CHECK=1`

## Quick Start

```bash
# Authenticate
fasci login

# List campaigns
fasci campaigns list

# List boosts
fasci boosts list

# Check subscription
fasci subscriptions me

# System status
fasci status
```

## Commands

| Command | Description |
|---------|-------------|
| `fasci login` | Authenticate with fasci |
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

## Configuration

Config stored at `~/.fasci/config.yaml`:
```yaml
api_key: your-api-key
api_url: http://localhost:8001
```

Or use environment variables:
- `FASCI_API_KEY`
- `FASCI_API_URL`

## Output Formats

```bash
fasci campaigns list --output json    # JSON output
fasci campaigns list --quiet          # IDs only
```
