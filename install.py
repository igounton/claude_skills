#!/usr/bin/env -S uv --quiet run --active --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer>=0.19.2",  # Typer includes Rich
# ]
# ///
"""Skill installation script for Claude Code.

Discovers all skills in the repository and creates symlinks in ~/.claude/skills/.
"""

from collections import Counter
from enum import StrEnum
from pathlib import Path
from typing import Annotated, NoReturn, assert_never

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Console setup
console = Console()
error_console = Console(stderr=True, style="bold red")

# Application setup
app = typer.Typer(name="install", help="Install Claude Code skills from this repository", rich_markup_mode="rich")


class InstallStatus(StrEnum):
    """Installation status for a skill."""

    ALREADY_INSTALLED = "already_installed"
    NEWLY_INSTALLED = "newly_installed"
    SKIPPED = "skipped"
    ERROR = "error"


class SkillInstaller:
    """Manages skill discovery and installation.

    Args:
        repo_root: Root directory of the skills repository
        target_dir: Target directory for skill symlinks (default: ~/.claude/skills/)
    """

    def __init__(self, repo_root: Path, target_dir: Path | None = None) -> None:
        """Initialize skill installer.

        Args:
            repo_root: Root directory of the skills repository
            target_dir: Target directory for skill symlinks
        """
        self.repo_root = repo_root
        self.target_dir = target_dir or Path.home() / ".claude" / "skills"

    def discover_skills(self) -> list[Path]:
        """Discover all skills by finding directories containing SKILL.md.

        Returns:
            List of skill directory paths

        Raises:
            ValueError: If repository root doesn't exist
        """
        if not self.repo_root.exists():
            msg = f"Repository root does not exist: {self.repo_root}"
            raise ValueError(msg)

        # Find all SKILL.md files and get their parent directories
        skill_files = list(self.repo_root.glob("*/SKILL.md"))
        return [skill_file.parent for skill_file in skill_files]

    def is_correctly_installed(self, skill_dir: Path) -> bool:
        """Check if skill is already correctly symlinked.

        Args:
            skill_dir: Skill directory path in repository

        Returns:
            True if symlink exists and points to correct location
        """
        skill_name = skill_dir.name
        symlink_path = self.target_dir / skill_name

        # Check existence and symlink status
        if not symlink_path.exists() or not symlink_path.is_symlink():
            return False

        # Check if symlink points to the correct location
        try:
            return symlink_path.resolve() == skill_dir.resolve()
        except (OSError, RuntimeError):
            return False

    def install_skill(self, skill_dir: Path) -> tuple[InstallStatus, str]:
        """Install a skill by creating a symlink.

        Args:
            skill_dir: Skill directory path in repository

        Returns:
            Tuple of (status, message)
        """
        skill_name = skill_dir.name
        symlink_path = self.target_dir / skill_name

        # Check if already correctly installed
        if self.is_correctly_installed(skill_dir):
            return (InstallStatus.ALREADY_INSTALLED, "Already correctly symlinked")

        # Handle existing symlink/file/directory at target
        if symlink_path.exists() or symlink_path.is_symlink():
            try:
                # Remove broken or incorrect symlink
                symlink_path.unlink()
            except OSError as e:
                return (InstallStatus.ERROR, f"Failed to remove existing link: {e}")

        # Create target directory if needed
        try:
            self.target_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return (InstallStatus.ERROR, f"Failed to create target directory: {e}")

        # Create symlink
        try:
            symlink_path.symlink_to(skill_dir)
        except OSError as e:
            return (InstallStatus.ERROR, f"Failed to create symlink: {e}")
        else:
            return (InstallStatus.NEWLY_INSTALLED, "Successfully installed")


def display_results(results: dict[str, tuple[InstallStatus, str]]) -> None:
    """Display installation results in a formatted table.

    Args:
        results: Dictionary mapping skill names to (status, message) tuples
    """
    table = Table(title=":electric_plug: Skill Installation Results")
    table.add_column("Skill", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("Details", style="white")

    for skill_name, (status, message) in sorted(results.items()):
        match status:
            case InstallStatus.ALREADY_INSTALLED:
                status_icon = "[green]:white_check_mark:[/green]"
                status_text = "Already Installed"
            case InstallStatus.NEWLY_INSTALLED:
                status_icon = "[green]:sparkles:[/green]"
                status_text = "Newly Installed"
            case InstallStatus.SKIPPED:
                status_icon = "[yellow]:warning:[/yellow]"
                status_text = "Skipped"
            case InstallStatus.ERROR:
                status_icon = "[red]:cross_mark:[/red]"
                status_text = "Error"
            case _ as unreachable:
                assert_never(unreachable)

        table.add_row(skill_name, f"{status_icon} {status_text}", message)

    console.print(table)

    # Print summary
    total = len(results)
    status_counts = Counter(status for status, _ in results.values())
    already_installed = status_counts[InstallStatus.ALREADY_INSTALLED]
    newly_installed = status_counts[InstallStatus.NEWLY_INSTALLED]
    errors = status_counts[InstallStatus.ERROR]

    summary_style = "green" if errors == 0 else "yellow"
    summary = (
        f"[{summary_style}]Summary:[/{summary_style}] "
        f"{total} skills processed, "
        f"{already_installed} already installed, "
        f"{newly_installed} newly installed"
    )

    if errors > 0:
        summary += f", [red]{errors} errors[/red]"

    console.print()
    console.print(Panel(summary, border_style=summary_style))


def _exit_no_skills() -> NoReturn:
    """Exit when no skills found (abstracted for TRY301)."""
    raise typer.Exit(0)


def _exit_with_errors() -> NoReturn:
    """Exit when installation errors occurred (abstracted for TRY301)."""
    raise typer.Exit(1)


@app.command()
def main(
    repo_path: Annotated[
        Path,
        typer.Option(
            "--repo", "-r", help="Repository root path (default: script directory)", rich_help_panel="Configuration"
        ),
    ] = Path(__file__).parent,
    target_path: Annotated[
        Path | None,
        typer.Option(
            "--target",
            "-t",
            help="Target directory for symlinks (default: ~/.claude/skills/)",
            rich_help_panel="Configuration",
        ),
    ] = None,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run", "-n", help="Show what would be done without making changes", rich_help_panel="Options"
        ),
    ] = False,
) -> None:
    """Install all skills from the repository to ~/.claude/skills/.

    Discovers skills by finding directories containing SKILL.md files,
    then creates symlinks in the target directory. Skips skills that
    are already correctly installed.
    """
    try:
        installer = SkillInstaller(repo_path, target_path)

        # Discover skills
        console.print(f"[cyan]Discovering skills in:[/cyan] {installer.repo_root}")
        skills = installer.discover_skills()

        if not skills:
            console.print("[yellow]No skills found in repository[/yellow]")
            _exit_no_skills()
            return  # For type checker

        console.print(f"[green]Found {len(skills)} skills[/green]")
        console.print()

        # Show dry-run notice if applicable
        if dry_run:
            console.print(Panel("[yellow]DRY RUN MODE - No changes will be made[/yellow]", border_style="yellow"))
            console.print()

        # Install each skill
        results: dict[str, tuple[InstallStatus, str]] = {}
        for skill_dir in skills:
            skill_name = skill_dir.name
            if dry_run:
                # In dry run, just check status
                if installer.is_correctly_installed(skill_dir):
                    results[skill_name] = (InstallStatus.ALREADY_INSTALLED, "Would skip (already installed)")
                else:
                    results[skill_name] = (InstallStatus.NEWLY_INSTALLED, "Would install")
            else:
                status, message = installer.install_skill(skill_dir)
                results[skill_name] = (status, message)

        # Display results
        display_results(results)

        # Exit with error code if any installations failed
        error_count = sum(1 for s, _ in results.values() if s == InstallStatus.ERROR)
        if error_count > 0:
            _exit_with_errors()
            return  # For type checker

    except ValueError as e:
        error_panel = Panel(
            f"[bold red]Configuration Error:[/bold red]\n{e!s}",
            title=":cross_mark: Installation Failed",
            border_style="red",
        )
        error_console.print(error_panel)
        raise typer.Exit(2) from e
    except Exception as e:
        error_panel = Panel(
            f"[bold red]Unexpected Error:[/bold red]\n{e!s}",
            title=":cross_mark: Installation Failed",
            border_style="red",
        )
        error_console.print(error_panel)
        raise typer.Exit(1) from e


if __name__ == "__main__":
    app()
