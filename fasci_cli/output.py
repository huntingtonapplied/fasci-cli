"""Output helpers for fasci CLI."""

import json
import sys

import click
from rich.console import Console


def get_console(ctx=None):
    return Console(stderr=False)


def is_json(ctx):
    if ctx and ctx.obj:
        return ctx.obj.get("output") == "json"
    return False


def is_structured(ctx):
    if ctx and ctx.obj:
        return ctx.obj.get("output") in ("json", "yaml")
    return False


def print_json(data):
    click.echo(json.dumps(data, indent=2, default=str))


def print_structured(ctx, data):
    output = ctx.obj.get("output", "json") if ctx and ctx.obj else "json"
    if output == "yaml":
        import yaml
        click.echo(yaml.dump(data, default_flow_style=False))
    else:
        print_json(data)
