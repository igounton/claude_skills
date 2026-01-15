#!/usr/bin/env -S uv --quiet run --active --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer>=0.19.2",
# ]
# ///
"""Plugin installation script for Claude Code marketplace.

Discovers all plugins in the repository and creates symlinks for:
- Skills to ~/.claude/skills/
- Commands to ~/.claude/commands/
- Agents to ~/.claude/agents/
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
error_console = Console(stderr=True, style="bold red")

app = typer.Typer(
    name="install",
    help="Install Claude Code plugins from this repository",
    rich_markup_mode="rich",
)


class InstallStatus(StrEnum):
    """Installation status for a component."""

    ALREADY_INSTALLED = "already_installed"
    NEWLY_INSTALLED = "newly_installed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class PluginConfig:
    """Configuration from plugin.json."""

    name: str
    description: str
    version: str
    skills: list[str] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)
    agents: list[str] = field(default_factory=list)


@dataclass
class InstallResult:
    """Result of installing a component."""

    status: InstallStatus
    message: str


class PluginInstaller:
    """Manages plugin discovery and installation.

    Args:
        repo_root: Root directory of the plugins repository
        skills_dir: Target directory for skill symlinks
        commands_dir: Target directory for command symlinks
        agents_dir: Target directory for agent symlinks
    """

    def __init__(
        self,
        repo_root: Path,
        skills_dir: Path | None = None,
        commands_dir: Path | None = None,
        agents_dir: Path | None = None,
    ) -> None:
        """Initialize plugin installer.

        Args:
            repo_root: Root directory of the plugins repository
            skills_dir: Target directory for skill symlinks
            commands_dir: Target directory for command symlinks
            agents_dir: Target directory for agent symlinks
        """
        self.repo_root = repo_root
        self.plugins_dir = repo_root / "plugins"
        self.skills_dir = skills_dir or Path.home() / ".claude" / "skills"
        self.commands_dir = commands_dir or Path.home() / ".claude" / "commands"
        self.agents_dir = agents_dir or Path.home() / ".claude" / "agents"

    def discover_plugins(self) -> list[Path]:
        """Discover all plugin directories.

        Returns:
            List of plugin directory paths

        Raises:
            ValueError: If plugins directory doesn't exist
        """
        if not self.plugins_dir.exists():
            msg = f"Plugins directory does not exist: {self.plugins_dir}"
            raise ValueError(msg)

        return sorted([
            d
            for d in self.plugins_dir.iterdir()
            if d.is_dir() and (d / ".claude-plugin" / "plugin.json").exists()
        ])

    def load_plugin_config(self, plugin_dir: Path) -> PluginConfig | None:
        """Load plugin configuration from plugin.json.

        Args:
            plugin_dir: Plugin directory path

        Returns:
            PluginConfig or None if loading fails
        """
        config_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not config_path.exists():
            return None

        try:
            with config_path.open(encoding="utf-8") as f:
                data = json.load(f)
                return PluginConfig(
                    name=data.get("name", plugin_dir.name),
                    description=data.get("description", ""),
                    version=data.get("version", "1.0.0"),
                    skills=data.get("skills", []),
                    commands=data.get("commands", []),
                    agents=data.get("agents", []),
                )
        except (json.JSONDecodeError, OSError):
            return None

    def is_correctly_symlinked(self, source: Path, target: Path) -> bool:
        """Check if target is correctly symlinked to source.

        Args:
            source: Source directory path
            target: Target symlink path

        Returns:
            True if symlink exists and points to correct location
        """
        if not target.exists() or not target.is_symlink():
            return False
        try:
            return target.resolve() == source.resolve()
        except (OSError, RuntimeError):
            return False

    def create_symlink(
        self, source: Path, target_dir: Path, target_name: str, dry_run: bool = False
    ) -> InstallResult:
        """Create a symlink for a component.

        Args:
            source: Source directory path
            target_dir: Target directory for symlink
            target_name: Name for the symlink
            dry_run: If True, just report what would be done

        Returns:
            InstallResult with status and message
        """
        target = target_dir / target_name

        if self.is_correctly_symlinked(source, target):
            return InstallResult(
                InstallStatus.ALREADY_INSTALLED, "Already correctly symlinked"
            )

        if dry_run:
            return InstallResult(InstallStatus.NEWLY_INSTALLED, "Would install")

        # Handle existing symlink/file/directory at target
        if target.exists() or target.is_symlink():
            try:
                target.unlink()
            except OSError as e:
                return InstallResult(
                    InstallStatus.ERROR, f"Failed to remove existing link: {e}"
                )

        # Create target directory if needed
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return InstallResult(
                InstallStatus.ERROR, f"Failed to create target directory: {e}"
            )

        # Create symlink
        try:
            target.symlink_to(source)
            return InstallResult(
                InstallStatus.NEWLY_INSTALLED, "Successfully installed"
            )
        except OSError as e:
            return InstallResult(InstallStatus.ERROR, f"Failed to create symlink: {e}")

    def install_plugin(
        self, plugin_dir: Path, dry_run: bool = False
    ) -> dict[str, InstallResult]:
        """Install all components from a plugin.

        Args:
            plugin_dir: Plugin directory path
            dry_run: If True, just report what would be done

        Returns:
            Dictionary mapping component names to InstallResults
        """
        results: dict[str, InstallResult] = {}

        config = self.load_plugin_config(plugin_dir)
        if config is None:
            results[plugin_dir.name] = InstallResult(
                InstallStatus.ERROR, "Failed to load plugin.json"
            )
            return results

        # Install skills
        for skill_path in config.skills:
            skill_dir = plugin_dir / skill_path.lstrip("./")
            if skill_dir.exists():
                skill_name = skill_dir.name
                result = self.create_symlink(
                    skill_dir, self.skills_dir, skill_name, dry_run
                )
                results[f"skill:{skill_name}"] = result

        # Install commands (symlink individual .md files)
        for cmd_path in config.commands:
            cmd_dir = plugin_dir / cmd_path.lstrip("./")
            if cmd_dir.exists() and cmd_dir.is_dir():
                for cmd_file in cmd_dir.glob("*.md"):
                    result = self.create_symlink(
                        cmd_file, self.commands_dir, cmd_file.name, dry_run
                    )
                    results[f"command:{cmd_file.stem}"] = result

        # Install agents (symlink individual .md files)
        for agent_path in config.agents:
            agent_dir = plugin_dir / agent_path.lstrip("./")
            if agent_dir.exists() and agent_dir.is_dir():
                for agent_file in agent_dir.glob("*.md"):
                    result = self.create_symlink(
                        agent_file, self.agents_dir, agent_file.name, dry_run
                    )
                    results[f"agent:{agent_file.stem}"] = result

        return results


def _exit_no_plugins() -> None:
    """Exit when no plugins found."""
    raise typer.Exit(0)


def _exit_with_errors() -> None:
    """Exit when installation errors occurred."""
    raise typer.Exit(1)


def display_results(results: dict[str, dict[str, InstallResult]]) -> None:
    """Display installation results in a formatted table.

    Args:
        results: Dictionary mapping plugin names to component results
    """
    table = Table(title=":electric_plug: Plugin Installation Results")
    table.add_column("Plugin", style="cyan", no_wrap=True)
    table.add_column("Component", style="magenta")
    table.add_column("Status")
    table.add_column("Details", style="white")

    status_icons = {
        InstallStatus.ALREADY_INSTALLED: "[green]:white_check_mark:[/green] Already Installed",
        InstallStatus.NEWLY_INSTALLED: "[green]:sparkles:[/green] Newly Installed",
        InstallStatus.SKIPPED: "[yellow]:warning:[/yellow] Skipped",
        InstallStatus.ERROR: "[red]:cross_mark:[/red] Error",
    }

    for plugin_name, components in sorted(results.items()):
        first_row = True
        for component_name, result in sorted(components.items()):
            table.add_row(
                plugin_name if first_row else "",
                component_name,
                status_icons.get(result.status, str(result.status)),
                result.message,
            )
            first_row = False

    console.print(table)

    # Print summary
    all_results = [r for comp in results.values() for r in comp.values()]
    total = len(all_results)
    status_counts = Counter(r.status for r in all_results)

    already = status_counts[InstallStatus.ALREADY_INSTALLED]
    newly = status_counts[InstallStatus.NEWLY_INSTALLED]
    errors = status_counts[InstallStatus.ERROR]

    summary_style = "green" if errors == 0 else "yellow"
    summary = (
        f"[{summary_style}]Summary:[/{summary_style}] "
        f"{total} components processed, "
        f"{already} already installed, "
        f"{newly} newly installed"
    )

    if errors > 0:
        summary += f", [red]{errors} errors[/red]"

    console.print()
    console.print(Panel(summary, border_style=summary_style))


@app.command()
def main(
    repo_path: Annotated[
        Path,
        typer.Option(
            "--repo",
            "-r",
            help="Repository root path (default: script directory)",
            rich_help_panel="Configuration",
        ),
    ] = Path(__file__).parent,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            "-n",
            help="Show what would be done without making changes",
            rich_help_panel="Options",
        ),
    ] = False,
) -> None:
    """Install all plugins from the repository.

    Discovers plugins in plugins/ directory and creates symlinks for
    skills, commands, and agents in their respective ~/.claude/ directories.
    """
    try:
        installer = PluginInstaller(repo_path)

        console.print(f"[cyan]Discovering plugins in:[/cyan] {installer.plugins_dir}")
        plugins = installer.discover_plugins()

        if not plugins:
            console.print("[yellow]No plugins found in repository[/yellow]")
            _exit_no_plugins()

        console.print(f"[green]Found {len(plugins)} plugins[/green]")
        console.print()

        if dry_run:
            console.print(
                Panel(
                    "[yellow]DRY RUN MODE - No changes will be made[/yellow]",
                    border_style="yellow",
                )
            )
            console.print()

        # Install each plugin
        all_results: dict[str, dict[str, InstallResult]] = {}
        for plugin_dir in plugins:
            plugin_name = plugin_dir.name
            results = installer.install_plugin(plugin_dir, dry_run)
            all_results[plugin_name] = results

        display_results(all_results)

        # Exit with error code if any installations failed
        error_count = sum(
            1
            for comp in all_results.values()
            for r in comp.values()
            if r.status == InstallStatus.ERROR
        )
        if error_count > 0:
            _exit_with_errors()

    except ValueError as e:
        error_panel = Panel(
            f"[bold red]Configuration Error:[/bold red]\n{e!s}",
            title=":cross_mark: Installation Failed",
            border_style="red",
        )
        error_console.print(error_panel)
        raise typer.Exit(2) from e
    except typer.Exit:
        raise
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
