# Changelog

All notable changes to the Fasci CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Pre-1.0 policy:** Minor versions (0.x) may include breaking changes.

## [0.1.0] - Unreleased

### Added
- Initial release with `login`, `campaigns`, `boosts`, `subscriptions`, `metrics`, `status`, `doctor`, and `completion` commands
- `--verbose/-v` flag for INFO-level logging to stderr
- `--debug` flag for DEBUG-level logging (HTTP requests)
- `--ci` flag for CI/CD pipeline usage (no color, no spinners, no prompts); auto-detected from `CI`, `GITHUB_ACTIONS`, `GITLAB_CI` env vars
- `fasci doctor` command — checks Python, config, API connectivity, auth, and shell completion
- Distinct exit codes: 2 (auth), 3 (not found), 4 (validation), 5 (network), 6 (server), 7 (duplicate), 130 (SIGINT), 143 (SIGTERM)
- Config validation with typo detection (`did you mean 'api_key'?`) on startup
- Configurable request timeout via `FASCI_TIMEOUT` env var or `timeout` config key
- SIGTERM signal handling across all commands (clean exit with code 143)
- Top-level KeyboardInterrupt handler as safety net for all commands
- Non-blocking version update check (background thread, 24h throttle, disabled in CI)
- Rich terminal output with table, JSON, and YAML formats
- Shell completion for bash, zsh, and fish
- Nuitka standalone binary builds

### Notes
- Configuration via `~/.fasci/config.yaml` or `FASCI_API_KEY` / `FASCI_API_URL` env vars
- Default API URL is `https://api.fasci.app`
