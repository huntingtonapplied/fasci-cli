"""fasci login — authenticate and store API key."""

import click
from rich.panel import Panel
from fasci_cli.config import save_config, load_config, get_api_url
from fasci_cli.api import FasciClient, APIError
from fasci_cli.output import get_console
from fasci_cli.exit_codes import EXIT_VALIDATION


@click.command()
@click.option("--key", default=None, help="Your fasci API key (skips wizard)")
@click.option("--url", default=None, help="API URL (default: http://localhost:8003)")
@click.pass_context
def login(ctx, key: str, url: str):
    """Authenticate with the fasci platform.

    \b
    Examples:
        fasci login                     # interactive wizard
        fasci login --key fasci_abc123  # non-interactive
    """
    console = get_console(ctx)
    ci_mode = ctx.obj.get("ci", False) if ctx.obj else False

    if not key and ci_mode:
        click.echo("✗ --key is required in CI mode: fasci login --key <key>", err=True)
        raise SystemExit(EXIT_VALIDATION)

    if not key:
        click.echo()
        click.echo("  Welcome to fasci!")
        click.echo()
        click.echo("  To get your API key:")
        click.echo("    1. Go to your fasci instance /account")
        click.echo("    2. Click the Developer tab")
        click.echo("    3. Copy your API key")
        click.echo()
        key = click.prompt("  API Key", hide_input=True)
        if not url:
            use_custom = click.confirm("  Use a custom API URL?", default=False)
            if use_custom:
                url = click.prompt("  API URL", default="http://localhost:8003")

    key = key.strip()
    config = load_config()
    config["api_key"] = key
    if url:
        config["api_url"] = url.strip()
    save_config(config)

    api_url = url or get_api_url()
    click.echo(f"✓ API key saved to ~/.fasci/config.yaml")
    click.echo(f"  API URL: {api_url}")

    try:
        client = FasciClient(api_key=key, api_url=api_url)
        campaign_list = client.list_campaigns()
        console.print(Panel(
            f"✓ Authenticated — {len(campaign_list)} campaign(s) found\n\n"
            "  [dim]fasci campaigns list[/dim]         list your campaigns\n"
            "  [dim]fasci boosts list[/dim]            list your boosts\n"
            "  [dim]fasci subscriptions me[/dim]    view your subscription",
            title="Connected",
            border_style="green",
            expand=False,
        ))
    except Exception as e:
        click.echo(f"⚠ Key saved but verification failed: {e}", err=True)
        click.echo("  Check your key and try again: fasci login", err=True)
