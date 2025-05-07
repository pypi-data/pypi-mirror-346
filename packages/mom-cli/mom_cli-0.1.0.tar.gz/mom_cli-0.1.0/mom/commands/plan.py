import os
import json
import click
from pathlib import Path
from datetime import datetime
from typing import Optional


@click.command()
def plan():
    """Start your session with a plan"""

    click.echo("mom says: What’s the plan for today, sweetie?\n")

    goal = click.prompt(
        "🥅 What’s your main goal for this session", default="", show_default=False
    )

    click.echo("\n🗂️ Tell me which file or part you’ll focus on.")
    click.echo("Type a filename (with path or extension) and I’ll try to match it.")
    click.echo(
        "Or write something abstract like 'refactor engine' and I’ll save it as a 'part'.\n"
    )

    matched_file: Optional[str] = ""
    matched_part: Optional[str] = ""

    while True:
        file_or_part = click.prompt("📌 File or part", default="", show_default=False)

        if not file_or_part:
            break

        if "/" in file_or_part or "." in file_or_part:
            matches = [
                str(p)
                for p in Path(".").rglob("*")
                if file_or_part in str(p)
                and not any(
                    part in str(p) for part in [".git", ".venv", "__pycache__", ".mom"]
                )
            ]
            if not matches:
                click.echo(
                    "❌ That file doesn’t exist, sweetie. Want to try again, but this time *carefully*?"
                )
                continue
            elif len(matches) == 1:
                matched_file = matches[0]
                break
            else:
                click.echo("\nFound multiple files:")
                for idx, path in enumerate(matches, 1):
                    click.echo(f"{idx}. {path}")
                choice = click.prompt("Which one do you mean?", type=int)
                matched_file = matches[choice - 1]
                break
        else:
            matched_part = file_or_part
            break

    reminder = click.prompt(
        "🧠 Any reminder you want mom to repeat later", default="", show_default=False
    )

    plan_data = {
        "goal": goal,
        "file": matched_file,
        "part": matched_part,
        "reminder": reminder,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }

    mom_dir = Path(".mom")
    mom_dir.mkdir(exist_ok=True)
    with open(mom_dir / "plan.json", "w", encoding="utf-8") as f:
        json.dump(plan_data, f, indent=4)

    click.echo("\n📋 Plan saved!")

    if not goal:
        click.echo("🥱 No goal? Don't make me come over there.")
    else:
        click.echo(f"✅ Goal set: {goal}")

    if matched_file:
        click.echo(f"📁 File selected: {matched_file}")
    elif matched_part:
        click.echo(f"🔍 Part selected: {matched_part}")
    else:
        click.echo("📂 Not even a file or a part? So you're planning to plan?")

    if not reminder:
        click.echo("🧠 No reminder? Brave. Or forgetful.")
    else:
        click.echo(f"📌 I’ll remind you: {reminder}")

    click.echo("\nI believe in you. But I’ll be watching. 💅")


# Public utility to get the age of the plan in minutes
def get_plan_age_minutes():
    """
    Returns the age of the current plan in minutes, or None if no plan is found.
    """
    plan_path = Path(".mom/plan.json")
    if not plan_path.exists():
        return None

    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        ts = data.get("created_at")
        if not ts:
            return None
        created_at = datetime.fromisoformat(ts.replace("Z", ""))
        delta = datetime.utcnow() - created_at
        return int(delta.total_seconds() / 60)
    except Exception:
        return None
