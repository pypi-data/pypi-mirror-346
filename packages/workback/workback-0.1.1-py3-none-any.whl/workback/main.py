"""Main entry point for the WorkBack CLI."""

import typer
from typing import Optional

from workback.tui.app import WorkBack

app = typer.Typer(
    name="workback",
    help="A terminal-based AI chat interface",
    add_completion=False,
)


@app.command()
def main(
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug mode",
    ),
    model: Optional[str] = typer.Option(
        None,
        "--model",
        "-m",
        help="Specify which AI model to use",
    ),
) -> None:
    """Launch the WorkBack TUI."""
    workback = WorkBack()
    workback.run()


if __name__ == "__main__":
    app()