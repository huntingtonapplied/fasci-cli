"""fasci status — show system status and recent activity."""

import click
from rich.panel import Panel
from fasci_cli.api import FasciClient, AuthError, APIError
from fasci_cli.output import get_console, is_json, print_json
from fasci_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.command()
@click.pass_context
def status(ctx):
    """Show fasci system status and recent activity."""
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
        campaigns = client.list_campaigns(params={"limit": 5})
        boosts = client.list_boosts(params={"limit": 5})
        metrics = client.get_portfolio_metrics()
        subscription = client.get_my_subscription()
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json({
            "campaigns": campaigns[:5] if campaigns else [],
            "boosts": boosts[:5] if boosts else [],
            "metrics": metrics,
            "subscription": subscription,
        })
        return

    console = get_console(ctx)

    # Subscription status
    if subscription:
        console.print(Panel(
            f"Status: {subscription.get('status', 'unknown')}\n"
            f"Tier: {subscription.get('tier_name', 'N/A')}",
            title="Subscription",
            border_style="green" if subscription.get("status") == "active" else "yellow",
            expand=False,
        ))

    # Campaigns summary
    if campaigns:
        click.echo(f"\nCampaigns ({len(campaigns)} recent):")
        for c in campaigns[:5]:
            click.echo(f"  • {c.get('name', 'Unknown')} — {c.get('status', 'unknown')}")

    # Boosts summary
    if boosts:
        click.echo(f"\nBoosts ({len(boosts)} recent):")
        for b in boosts[:5]:
            click.echo(f"  • {b.get('name', 'Unknown')} — {b.get('status', 'unknown')}")

    # Portfolio metrics
    if metrics:
        click.echo(f"\nPortfolio Metrics:")
        click.echo(f"  Total Campaigns: {metrics.get('total_campaigns', 'N/A')}")
        click.echo(f"  Active Boosts: {metrics.get('active_boosts', 'N/A')}")
