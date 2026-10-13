"""fasci campaigns — manage campaigns."""

import click
from rich.table import Table
from fasci_cli.api import FasciClient, AuthError, APIError
from fasci_cli.output import get_console, is_json, print_json
from fasci_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def campaigns(ctx):
    """Manage campaigns."""
    pass


@campaigns.command("list")
@click.option("--limit", "-n", default=20, show_default=True, help="Max results to return")
@click.option("--status", "-s", default=None, help="Filter by status")
@click.option("--quiet", "-q", is_flag=True, help="Print only campaign IDs")
@click.pass_context
def campaigns_list(ctx, limit, status, quiet):
    """List campaigns."""
    json_mode = is_json(ctx)

    try:
        client = FasciClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    params = {"limit": limit} if limit != 20 else {}
    if status:
        params["status"] = status

    try:
        campaign_list = client.list_campaigns(params=params)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(campaign_list)
        return

    if not campaign_list:
        click.echo("No campaigns found.")
        return

    if quiet:
        for c in campaign_list:
            click.echo(c.get("id", ""))
        return

    console = get_console(ctx)
    table = Table(show_edge=False, pad_edge=False, box=None)
    table.add_column("Name", style="cyan", min_width=20)
    table.add_column("Status", min_width=12)
    table.add_column("ID", style="dim")

    for c in campaign_list:
        table.add_row(
            c.get("name", "Unknown")[:36],
            c.get("status", "unknown"),
            c.get("id", "")[:8],
        )

    console.print(table)


@campaigns.command("get")
@click.argument("campaign_id")
@click.pass_context
def campaigns_get(ctx, campaign_id):
    """Get details of a specific campaign."""
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
        campaign = client.get_campaign(campaign_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(campaign)
        return

    console = get_console(ctx)
    console.print(f"[bold]{campaign.get('name', 'Unknown')}[/bold]")
    console.print(f"  ID: {campaign.get('id', '')}")
    console.print(f"  Status: {campaign.get('status', '')}")


@campaigns.command("delete")
@click.argument("campaign_id")
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt")
@click.pass_context
def campaigns_delete(ctx, campaign_id, yes):
    """Delete a campaign."""
    json_mode = is_json(ctx)
    ci_mode = ctx.obj.get("ci", False) if ctx.obj else False

    if not yes and not ci_mode:
        click.confirm(f"Delete campaign {campaign_id}? This cannot be undone.", abort=True)

    try:
        client = FasciClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    try:
        client.delete_campaign(campaign_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json({"deleted": campaign_id})
    else:
        click.echo(f"✓ Deleted campaign {campaign_id}")
