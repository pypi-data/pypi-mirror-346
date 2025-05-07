import click
from datetime import datetime
from mom.utils.style import console
from mom.utils.git import (
    get_uncommitted_files,
    get_last_commit_time,
    parse_git_status_lines,
)


@click.command()
def status():
    """Check the health of your current codebase state."""
    console.print("mom is checking your codebase... 🩺", style="mom.info")

    uncommitted, minutes = get_status_summary()

    if uncommitted is None:
        console.print("⚠️ This is not a Git repository.", style="mom.warning")
        return

    if uncommitted:
        console.print(
            f"✗ You have [bold red]{len(uncommitted)}[/bold red] uncommitted file(s).",
            style="mom.error",
        )

        parsed = parse_git_status_lines(uncommitted)
        for code, fname in parsed:
            if code == "M":
                style = "mom.warning"
                icon = "📝"
                label = "modified"
            elif code == "A":
                style = "mom.success"
                icon = "➕"
                label = "added"
            elif code == "??":
                style = "mom.info"
                icon = "❓"
                label = "untracked"
            else:
                style = "mom.italic"
                icon = "🔧"
                label = code

            console.print(
                f" {icon} [bold]{fname}[/bold] → [italic]{label}[/italic]", style=style
            )
    else:
        console.print("✓ No uncommitted changes. Good job!", style="mom.success")

    if minutes is not None:
        if minutes < 1:
            console.print("⏱️ Just committed! You’re on fire 🔥", style="mom.success")
        elif minutes < 60:
            console.print(
                f"⏱️ Last commit was [bold]{minutes}[/bold] minute(s) ago.",
                style="mom.success",
            )
        else:
            hours = minutes // 60
            mins = minutes % 60
            console.print(
                f"⏱️ Last commit was [bold]{hours}h {mins}m[/bold] ago.",
                style="mom.warning",
            )
    else:
        console.print(
            "⏱️ This repository has no commits yet. Time to make history!",
            style="mom.warning",
        )

    # Final message from mom
    console.print("Don't forget to commit when you're ready. ❤️", style="mom.italic")


def get_status_summary():
    """
    Returns a tuple (uncommitted_files, minutes_since_commit or None)
    """
    uncommitted = get_uncommitted_files()
    if uncommitted is None:
        return None, None

    commit_time = get_last_commit_time()
    if commit_time:
        delta = datetime.now() - commit_time
        minutes = int(delta.total_seconds() / 60)
        return uncommitted, minutes
    else:
        return uncommitted, None
