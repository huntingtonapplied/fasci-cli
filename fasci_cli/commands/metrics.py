"""fasci metrics — view portfolio and system metrics."""

import click
from fasci_cli.api import FasciClient, AuthError, APIError
from fasci_cli.output import get_console, is_json, print_json
from fasci_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def metrics(ctx):
    """View portfolio and system metrics."""
    pass


@metrics.command("portfolio")
@click.pass_context
def metrics_portfolio(ctx):
    """Get portfolio metrics."""
    json_mode = is_json(ctx)

    try:
        client = FasciClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    try:
        data = client.get_portfolio_metrics()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(data)
        return

    console = get_console(ctx)
    console.print("[bold]Portfolio Metrics[/bold]")
    console.print(f"  Total Campaigns: {data.get('total_campaigns', 'N/A')}")
    console.print(f"  Active Boosts: {data.get('active_boosts', 'N/A')}")
    console.print(f"  Total Users: {data.get('total_users', 'N/A')}")
