import json
from pathlib import Path
from datetime import datetime
import click
from mom.utils.style import console
from dateutil.parser import isoparse


@click.command()
def focus():
    """Remind yourself what you're supposed to be working on."""
    plan_path = Path(".mom/plan.json")
    if not plan_path.exists():
        console.print("No plan found. Did you forget to ask mom?", style="mom.warning")
        return

    with open(plan_path, "r", encoding="utf-8") as f:
        try:
            plan = json.load(f)
        except json.JSONDecodeError:
            console.print(
                "That plan is a mess. Mom can’t even read it.", style="mom.error"
            )
            return

    console.print("mom says: Stay focused. Here’s your plan 👇\n", style="mom.info")

    if plan.get("goal"):
        console.print(f"🎯 Goal: [bold]{plan['goal']}[/bold]", style="mom.success")
    else:
        console.print("🎯 No goal? You better not be winging it.", style="mom.warning")

    if plan.get("file"):
        console.print(
            f"📁 File to work on: [italic]{plan['file']}[/italic]", style="mom.italic"
        )
    elif plan.get("part"):
        console.print(
            f"🧩 Focus area: [italic]{plan['part']}[/italic]", style="mom.italic"
        )
    else:
        console.print(
            "📂 Nothing? You sure this is a real session?", style="mom.warning"
        )

    if plan.get("reminder"):
        console.print(f"📌 Reminder: {plan['reminder']}", style="mom.info")

    if ts := plan.get("created_at"):
        try:
            created_at = isoparse(ts)
            delta = datetime.now(created_at.tzinfo) - created_at
            minutes = int(delta.total_seconds() / 60)
            if minutes < 1:
                emoji = "🟢"
                msg = "Just now. No excuses for being off track."
                style = "mom.dim"
            elif minutes < 60:
                emoji = "🟢"
                msg = f"{minutes} minute(s) ago. Still fresh."
                style = "mom.dim"
            elif minutes < 1440:
                hours = minutes // 60
                emoji = "🟡"
                msg = f"{hours} hour(s) ago. Mom is watching."
                style = "mom.info"
            else:
                days = minutes // 1440
                emoji = "🔴"
                msg = f"{days} day(s) ago. Might want to revisit the plan."
                style = "mom.warning"

            console.print(f"{emoji} This plan was made: {msg}", style=style)
        except Exception:
            console.print(
                "⏱️ Couldn’t read the timestamp. Classic.", style="mom.warning"
            )
