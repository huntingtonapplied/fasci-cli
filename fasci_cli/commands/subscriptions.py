"""fasci subscriptions — manage subscriptions."""

import click
from rich.table import Table
from fasci_cli.api import FasciClient, AuthError, APIError
from fasci_cli.output import get_console, is_json, print_json
from fasci_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def subscriptions(ctx):
    """Manage subscriptions."""
    pass


@subscriptions.command("tiers")
@click.pass_context
def subscriptions_tiers(ctx):
    """List available subscription tiers."""
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
        tiers = client.list_subscription_tiers()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(tiers)
        return

    if not tiers:
        click.echo("No subscription tiers found.")
        return

    console = get_console(ctx)
    table = Table(show_edge=False, pad_edge=False, box=None)
    table.add_column("Name", style="cyan", min_width=20)
    table.add_column("Price", min_width=12)
    table.add_column("ID", style="dim")

    for t in tiers:
        table.add_row(
            t.get("name", "Unknown")[:36],
            f"${t.get('price', 0):.2f}",
            t.get("id", "")[:8],
        )

    console.print(table)


@subscriptions.command("me")
@click.pass_context
def subscriptions_me(ctx):
    """Get your current subscription."""
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
        sub = client.get_my_subscription()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(sub)
        return

    if not sub:
        click.echo("No active subscription found.")
        return

    console = get_console(ctx)
    console.print("[bold]Your Subscription[/bold]")
    console.print(f"  Status: {sub.get('status', 'unknown')}")
    console.print(f"  Tier: {sub.get('tier_name', 'N/A')}")
    console.print(f"  Renews: {sub.get('current_period_end', 'N/A')[:10]}")
