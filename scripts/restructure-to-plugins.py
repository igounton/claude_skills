#!/usr/bin/env -S uv --quiet run --active --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer>=0.19.2",
#     "pyyaml>=6.0",
# ]
# ///
"""Restructure claude_skills repository from flat skills to plugin marketplace format.

This script:
1. Creates plugins/{skill}/.claude-plugin/plugin.json for each skill
2. Creates plugins/{skill}/skills/{skill}/ directory structure
3. Moves skill content using git mv (preserves history)
4. Moves nested commands/agents to plugin root level
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
error_console = Console(stderr=True, style="bold red")

app = typer.Typer(
    name="restructure", help="Restructure claude_skills to plugin marketplace format"
)


@dataclass
class SkillMetadata:
    """Metadata extracted from SKILL.md frontmatter."""

    name: str
    description: str


@dataclass
class SkillContext:
    """Context for restructuring a single skill."""

    skill_dir: Path
    plugin_dir: Path
    skill_target_dir: Path
    metadata: SkillMetadata
    has_commands: bool
    has_agents: bool


def extract_frontmatter(skill_md_path: Path) -> SkillMetadata:
    """Extract YAML frontmatter from SKILL.md.

    Args:
        skill_md_path: Path to SKILL.md file

    Returns:
        SkillMetadata with name and description
    """
    content = skill_md_path.read_text(encoding="utf-8")
    default_name = skill_md_path.parent.name

    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return SkillMetadata(name=default_name, description="")

    frontmatter = match.group(1)
    name = default_name
    description = ""

    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip()

    desc_match = re.search(
        r"^description:\s*(.+?)(?=\n[a-z]+:|$)", frontmatter, re.MULTILINE | re.DOTALL
    )
    if desc_match:
        description = desc_match.group(1).strip()

    return SkillMetadata(name=name, description=description)


def create_plugin_json(ctx: SkillContext) -> None:
    """Create .claude-plugin/plugin.json for a plugin.

    Args:
        ctx: Skill context with all necessary information
    """
    claude_plugin_dir = ctx.plugin_dir / ".claude-plugin"
    claude_plugin_dir.mkdir(parents=True, exist_ok=True)

    plugin_json: dict[str, str | list[str]] = {
        "name": ctx.metadata.name,
        "description": ctx.metadata.description,
        "version": "1.0.0",
        "skills": [f"./skills/{ctx.metadata.name}"],
    }

    if ctx.has_commands:
        plugin_json["commands"] = ["./commands"]
    if ctx.has_agents:
        plugin_json["agents"] = ["./agents"]

    plugin_json_path = claude_plugin_dir / "plugin.json"
    with plugin_json_path.open("w", encoding="utf-8") as f:
        json.dump(plugin_json, f, indent=2)
        f.write("\n")


def find_git_executable() -> str:
    """Find the git executable path.

    Returns:
        Full path to git executable

    Raises:
        FileNotFoundError: If git is not found
    """
    git_path = shutil.which("git")
    if git_path is None:
        msg = "git executable not found in PATH"
        raise FileNotFoundError(msg)
    return git_path


def git_mv(src: Path, dst: Path, dry_run: bool = False) -> bool:
    """Move file/directory using git mv.

    Args:
        src: Source path
        dst: Destination path
        dry_run: If True, just print what would be done

    Returns:
        True if successful
    """
    if dry_run:
        console.print(f"  [cyan]git mv[/cyan] {src} -> {dst}")
        return True

    dst.parent.mkdir(parents=True, exist_ok=True)

    git_path = find_git_executable()
    result = subprocess.run(
        [git_path, "mv", str(src), str(dst)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        error_console.print(f"  [red]Error moving {src}:[/red] {result.stderr}")
        return False
    return True


def log_dry_run_info(ctx: SkillContext) -> None:
    """Log skill information during dry run.

    Args:
        ctx: Skill context with metadata
    """
    console.print(f"\n[bold cyan]Plugin: {ctx.skill_dir.name}[/bold cyan]")
    desc_preview = ctx.metadata.description[:50] if ctx.metadata.description else ""
    console.print(
        f"  Metadata: name={ctx.metadata.name}, description={desc_preview}..."
    )
    console.print(f"  Has commands: {ctx.has_commands}, Has agents: {ctx.has_agents}")


def move_skill_content(ctx: SkillContext, dry_run: bool) -> tuple[bool, str]:
    """Move main skill content to target directory.

    Args:
        ctx: Skill context
        dry_run: If True, just print what would be done

    Returns:
        Tuple of (success, error_message)
    """
    items_to_move = [
        item
        for item in ctx.skill_dir.iterdir()
        if item.name not in {"commands", "agents"} and not item.name.startswith(".")
    ]

    for item in items_to_move:
        dst = ctx.skill_target_dir / item.name
        if not git_mv(item, dst, dry_run):
            return False, f"Failed to move {item}"

    return True, ""


def move_special_directories(ctx: SkillContext, dry_run: bool) -> tuple[bool, str]:
    """Move commands and agents directories to plugin root.

    Args:
        ctx: Skill context
        dry_run: If True, just print what would be done

    Returns:
        Tuple of (success, error_message)
    """
    if ctx.has_commands:
        src = ctx.skill_dir / "commands"
        dst = ctx.plugin_dir / "commands"
        if not git_mv(src, dst, dry_run):
            return False, f"Failed to move commands from {ctx.skill_dir.name}"

    if ctx.has_agents:
        src = ctx.skill_dir / "agents"
        dst = ctx.plugin_dir / "agents"
        if not git_mv(src, dst, dry_run):
            return False, f"Failed to move agents from {ctx.skill_dir.name}"

    return True, ""


def cleanup_empty_directory(skill_dir: Path, dry_run: bool) -> None:
    """Remove empty skill directory after move.

    Args:
        skill_dir: Directory to clean up
        dry_run: If True, just print what would be done
    """
    if dry_run:
        console.print(f"  [yellow]Remove[/yellow] empty directory {skill_dir}")
        return

    remaining = list(skill_dir.iterdir())
    all_hidden = all(item.name.startswith(".") for item in remaining)

    if not remaining or all_hidden:
        for item in remaining:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        skill_dir.rmdir()


def restructure_skill(
    skill_dir: Path, plugins_dir: Path, dry_run: bool = False
) -> tuple[bool, str]:
    """Restructure a single skill into plugin format.

    Args:
        skill_dir: Current skill directory (e.g., ./uv)
        plugins_dir: Target plugins directory (e.g., ./plugins)
        dry_run: If True, just print what would be done

    Returns:
        Tuple of (success, message)
    """
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        return False, f"SKILL.md not found in {skill_dir}"

    ctx = SkillContext(
        skill_dir=skill_dir,
        plugin_dir=plugins_dir / skill_dir.name,
        skill_target_dir=plugins_dir / skill_dir.name / "skills" / skill_dir.name,
        metadata=extract_frontmatter(skill_md_path),
        has_commands=(skill_dir / "commands").is_dir(),
        has_agents=(skill_dir / "agents").is_dir(),
    )

    if dry_run:
        log_dry_run_info(ctx)
        console.print(
            f"  [green]Create[/green] {ctx.plugin_dir / '.claude-plugin' / 'plugin.json'}"
        )
    else:
        ctx.skill_target_dir.mkdir(parents=True, exist_ok=True)
        create_plugin_json(ctx)

    success, error = move_skill_content(ctx, dry_run)
    if not success:
        return False, error

    success, error = move_special_directories(ctx, dry_run)
    if not success:
        return False, error

    cleanup_empty_directory(ctx.skill_dir, dry_run)

    return True, "Successfully restructured"


def display_results(results: dict[str, tuple[bool, str]]) -> None:
    """Display restructure results in a table.

    Args:
        results: Dictionary mapping skill names to (success, message) tuples
    """
    console.print("\n")
    table = Table(title="Restructure Results")
    table.add_column("Skill", style="cyan")
    table.add_column("Status")
    table.add_column("Message")

    for skill_name, (success, message) in sorted(results.items()):
        status = (
            "[green]:white_check_mark:[/green]"
            if success
            else "[red]:cross_mark:[/red]"
        )
        table.add_row(skill_name, status, message)

    console.print(table)


@app.command()
def main(
    repo_path: Annotated[
        Path,
        typer.Option(
            "--repo",
            "-r",
            help="Repository root path (default: script parent directory)",
        ),
    ] = Path(__file__).parent.parent,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run", "-n", help="Show what would be done without making changes"
        ),
    ] = False,
) -> None:
    """Restructure skills repository to plugin marketplace format."""
    repo_path = repo_path.resolve()
    plugins_dir = repo_path / "plugins"

    console.print(
        Panel(f"[bold]Repository:[/bold] {repo_path}", title="Restructure to Plugins")
    )

    if dry_run:
        console.print(
            Panel(
                "[yellow]DRY RUN MODE - No changes will be made[/yellow]",
                border_style="yellow",
            )
        )

    skill_dirs = sorted([
        skill_md.parent
        for skill_md in repo_path.glob("*/SKILL.md")
        if not skill_md.parent.name.startswith(".")
        and skill_md.parent.name != "plugins"
    ])

    console.print(f"\n[green]Found {len(skill_dirs)} skills to restructure[/green]\n")

    results: dict[str, tuple[bool, str]] = {}
    for skill_dir in skill_dirs:
        success, message = restructure_skill(skill_dir, plugins_dir, dry_run)
        results[skill_dir.name] = (success, message)

    display_results(results)

    success_count = sum(1 for s, _ in results.values() if s)
    fail_count = len(results) - success_count

    if fail_count > 0:
        console.print(f"\n[red]Completed with {fail_count} errors[/red]")
        raise typer.Exit(1)
    console.print(f"\n[green]Successfully restructured {success_count} skills[/green]")


if __name__ == "__main__":
    app()
