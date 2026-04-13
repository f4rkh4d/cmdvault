"""CLI interface for cmdvault."""

from __future__ import annotations

import sys

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from cmdvault import __version__
from cmdvault.runner import find_placeholders, run
from cmdvault.search import search
from cmdvault.store import (
    add as store_add,
    export_all,
    get,
    import_all,
    list_all,
    remove,
    update,
)

console = Console()


def _format_command(cmd: str) -> Text:
    """Highlight placeholders in a command string."""
    text = Text(cmd)
    for name in find_placeholders(cmd):
        text.highlight_regex(rf"\{{\{{{name}\}}\}}", style="bold magenta")
    return text


def _print_table(entries: list[dict]) -> None:
    if not entries:
        console.print("[dim]No commands found.[/dim]")
        return

    table = Table(show_header=True, header_style="bold cyan", padding=(0, 1))
    table.add_column("ID", style="yellow", width=10)
    table.add_column("Command", no_wrap=False)
    table.add_column("Description", style="dim")
    table.add_column("Tags", style="green")

    for e in entries:
        table.add_row(
            e["id"],
            _format_command(e["command"]),
            e.get("description", ""),
            ", ".join(e.get("tags", [])),
        )
    console.print(table)


@click.group()
@click.version_option(__version__, prog_name="cmdvault")
def cli() -> None:
    """Save, search, and run your terminal commands."""


@cli.command()
@click.argument("command")
@click.option("-d", "--description", default="", help="Description of the command.")
@click.option("-t", "--tags", default="", help="Comma-separated tags.")
def add(command: str, description: str, tags: str) -> None:
    """Save a new command to the vault."""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    entry = store_add(command, description=description, tags=tag_list)
    console.print(f"[green]Saved[/green] with id [yellow]{entry['id']}[/yellow]")


@cli.command("list")
def list_cmd() -> None:
    """Show all saved commands."""
    _print_table(list_all())


@cli.command()
@click.argument("query")
def find(query: str) -> None:
    """Search commands by keyword, tag, or text."""
    entries = list_all()
    results = search(entries, query)
    _print_table(results)


@cli.command()
@click.argument("entry_id")
@click.option("--dry-run", is_flag=True, help="Print the command without executing.")
def run_cmd(entry_id: str, dry_run: bool) -> None:
    """Execute a saved command by its ID."""
    entry = get(entry_id)
    if not entry:
        console.print(f"[red]Command {entry_id} not found.[/red]")
        sys.exit(1)
    console.print(f"[dim]Running:[/dim] {_format_command(entry['command'])}")
    exit_code = run(entry["command"], dry_run=dry_run)
    if exit_code != 0:
        sys.exit(exit_code)


# register 'run' as the CLI name (can't use 'run' as Python function name — shadows import)
run_cmd.name = "run"


@cli.command()
@click.argument("entry_id")
@click.option("-c", "--command", "new_command", default=None, help="New command text.")
@click.option("-d", "--description", default=None, help="New description.")
@click.option("-t", "--tags", default=None, help="New comma-separated tags.")
def edit(entry_id: str, new_command: str | None, description: str | None, tags: str | None) -> None:
    """Edit a saved command."""
    fields: dict = {}
    if new_command is not None:
        fields["command"] = new_command
    if description is not None:
        fields["description"] = description
    if tags is not None:
        fields["tags"] = [t.strip() for t in tags.split(",") if t.strip()]

    if not fields:
        console.print("[dim]Nothing to update. Use --command, --description, or --tags.[/dim]")
        return

    result = update(entry_id, **fields)
    if result:
        console.print(f"[green]Updated[/green] [yellow]{entry_id}[/yellow]")
    else:
        console.print(f"[red]Command {entry_id} not found.[/red]")


@cli.command()
@click.argument("entry_id")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation.")
def rm(entry_id: str, yes: bool) -> None:
    """Remove a command from the vault."""
    entry = get(entry_id)
    if not entry:
        console.print(f"[red]Command {entry_id} not found.[/red]")
        sys.exit(1)
    if not yes:
        console.print(f"Delete: [bold]{entry['command']}[/bold]")
        if not click.confirm("Are you sure?"):
            return
    remove(entry_id)
    console.print(f"[green]Removed[/green] [yellow]{entry_id}[/yellow]")


@cli.command("export")
def export_cmd() -> None:
    """Export all commands as JSON to stdout."""
    click.echo(export_all())


@cli.command("import")
@click.argument("file", type=click.Path(exists=True))
def import_cmd(file: str) -> None:
    """Import commands from a JSON file."""
    from pathlib import Path

    data = Path(file).read_text(encoding="utf-8")
    count = import_all(data)
    console.print(f"[green]Imported {count} new command(s).[/green]")
