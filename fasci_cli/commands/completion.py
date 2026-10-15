"""Shell completion for fasci CLI."""

import click


@click.command()
@click.argument("shell", required=False, type=click.Choice(["bash", "zsh", "fish"], case_sensitive=False))
@click.pass_context
def completion(ctx, shell):
    """Generate shell completion script.

    \b
    Examples:
        fasci completion bash > ~/.bashrc
        fasci completion zsh >> ~/.zshrc
        fasci completion fish > ~/.config/fish/config.fish
    """
    if shell is None:
        import os
        shell = _detect_shell()

    if shell == "bash":
        click.echo("eval \"$(_FASCI_COMPLETE=bash_source fasci)\"")
    elif shell == "zsh":
        click.echo("eval \"$(_FASCI_COMPLETE=zsh_source fasci)\"")
    elif shell == "fish":
        click.echo("eval (env _FASCI_COMPLETE=fish_source fasci)")


def _detect_shell():
    import os
    shell = os.path.basename(os.getenv("SHELL", ""))
    if "bash" in shell:
        return "bash"
    elif "zsh" in shell:
        return "zsh"
    elif "fish" in shell:
        return "fish"
    return "bash"
