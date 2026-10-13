"""fasci boosts — manage boosts."""

import click
from rich.table import Table
from fasci_cli.api import FasciClient, AuthError, APIError
from fasci_cli.output import get_console, is_json, print_json
from fasci_cli.exit_codes import EXIT_AUTH, EXIT_GENERAL


@click.group()
@click.pass_context
def boosts(ctx):
    """Manage boosts."""
    pass


@boosts.command("list")
@click.option("--limit", "-n", default=20, show_default=True, help="Max results to return")
@click.option("--quiet", "-q", is_flag=True, help="Print only boost IDs")
@click.pass_context
def boosts_list(ctx, limit, quiet):
    """List boosts."""
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

    try:
        boost_list = client.list_boosts(params=params)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(boost_list)
        return

    if not boost_list:
        click.echo("No boosts found.")
        return

    if quiet:
        for b in boost_list:
            click.echo(b.get("id", ""))
        return

    console = get_console(ctx)
    table = Table(show_edge=False, pad_edge=False, box=None)
    table.add_column("Name", style="cyan", min_width=20)
    table.add_column("Status", min_width=12)
    table.add_column("ID", style="dim")

    for b in boost_list:
        table.add_row(
            b.get("name", "Unknown")[:36],
            b.get("status", "unknown"),
            b.get("id", "")[:8],
        )

    console.print(table)


@boosts.command("get")
@click.argument("boost_id")
@click.pass_context
def boosts_get(ctx, boost_id):
    """Get details of a specific boost."""
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
        boost = client.get_boost(boost_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(boost)
        return

    console = get_console(ctx)
    console.print(f"[bold]{boost.get('name', 'Unknown')}[/bold]")
    console.print(f"  ID: {boost.get('id', '')}")
    console.print(f"  Status: {boost.get('status', '')}")


@boosts.command("create")
@click.option("--name", required=True, help="Boost name")
@click.option("--amount", required=True, type=float, help="Boost amount")
@click.option("--campaign-id", required=True, help="Campaign ID")
@click.pass_context
def boosts_create(ctx, name, amount, campaign_id):
    """Create a new boost."""
    json_mode = is_json(ctx)

    try:
        client = FasciClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    data = {
        "name": name,
        "amount": amount,
        "campaign_id": campaign_id,
    }

    try:
        boost = client.create_boost(data)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json(boost)
        return

    click.echo(f"✓ Created boost: {boost.get('name', '')}")
    click.echo(f"  ID: {boost.get('id', '')}")


@boosts.command("cancel")
@click.argument("boost_id")
@click.option("--yes", "-y", is_flag=True, default=False, help="Skip confirmation prompt")
@click.pass_context
def boosts_cancel(ctx, boost_id, yes):
    """Cancel a boost."""
    json_mode = is_json(ctx)
    ci_mode = ctx.obj.get("ci", False) if ctx.obj else False

    if not yes and not ci_mode:
        click.confirm(f"Cancel boost {boost_id}?", abort=True)

    try:
        client = FasciClient()
    except AuthError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_AUTH)

    try:
        client.cancel_boost(boost_id)
    except APIError as e:
        if json_mode:
            print_json({"error": str(e)})
        else:
            click.echo(f"✗ {e}", err=True)
        raise SystemExit(EXIT_GENERAL)

    if json_mode:
        print_json({"cancelled": boost_id})
    else:
        click.echo(f"✓ Cancelled boost {boost_id}")
