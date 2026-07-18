"""fasci CLI — Campaign management from your terminal."""

import os
import signal
import sys

import click
from fasci_cli import __version__
from fasci_cli.log import setup_logging, logger
from fasci_cli.exit_codes import EXIT_GENERAL, EXIT_SIGINT, EXIT_SIGTERM
from fasci_cli.config import load_config, validate_config
from fasci_cli.update_check import UpdateChecker
from fasci_cli.commands.login import login
from fasci_cli.commands.campaigns import campaigns
from fasci_cli.commands.boosts import boosts
from fasci_cli.commands.subscriptions import subscriptions
from fasci_cli.commands.metrics import metrics
from fasci_cli.commands.status import status
from fasci_cli.commands.doctor import doctor
from fasci_cli.commands.completion import completion


@click.group()
@click.version_option(version=__version__, prog_name="fasci")
@click.option("--output", "-o", type=click.Choice(["table", "json", "yaml"]), default="table",
              help="Output format (default: table)")
@click.option("--no-color", is_flag=True, default=False, envvar="NO_COLOR",
              help="Disable colored output")
@click.option("--verbose", "-v", is_flag=True, default=False,
              help="Show informational messages (INFO level)")
@click.option("--debug", is_flag=True, default=False,
              help="Show debug messages including HTTP requests")
@click.option("--ci", is_flag=True, default=False,
              help="CI mode: no color, no spinners, no interactive prompts")
@click.pass_context
def cli(ctx, output, no_color, verbose, debug, ci):
    """fasci CLI — Campaign management from your terminal."""
    if not ci and (os.getenv("CI") or os.getenv("GITHUB_ACTIONS") or os.getenv("GITLAB_CI")):
        ci = True

    if ci:
        no_color = True

    ctx.ensure_object(dict)
    ctx.obj["output"] = output
    ctx.obj["no_color"] = no_color
    ctx.obj["verbose"] = verbose
    ctx.obj["debug"] = debug
    ctx.obj["ci"] = ci
    setup_logging(verbose=verbose, debug=debug)

    config = load_config()
    if config:
        warnings = validate_config(config)
        for w in warnings:
            click.echo(f"Warning: {w}", err=True)


cli.add_command(login)
cli.add_command(campaigns)
cli.add_command(boosts)
cli.add_command(subscriptions)
cli.add_command(metrics)
cli.add_command(status)
cli.add_command(doctor)
cli.add_command(completion)


_update_checker = UpdateChecker()


def main():
    """Entry point with top-level signal and exception handling."""
    signal.signal(signal.SIGTERM, lambda sig, frame: sys.exit(EXIT_SIGTERM))
    _update_checker.start()
    try:
        cli(standalone_mode=False)
    except click.exceptions.Exit as e:
        raise SystemExit(e.exit_code)
    except (KeyboardInterrupt, click.Abort):
        raise SystemExit(EXIT_SIGINT)
    except SystemExit:
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise SystemExit(EXIT_GENERAL)
    finally:
        _update_checker.notify_if_outdated()


if __name__ == "__main__":
    main()
