import click
import subprocess
import time
from mom.utils.style import console


@click.command()
def nag():
    try:
        output = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct"], text=True
        )
        last_commit_time = int(output.strip())
    except subprocess.CalledProcessError:
        console.print(
            "❌ Not a git repository. Mom can’t nag nothing.", style="mom.error"
        )
        return
    now = int(time.time())
    minutes_passed = (now - last_commit_time) // 60

    try:
        branch_output = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()

        if branch_output not in ["main", "dev"]:
            console.print(
                f"\n🌱 You are on branch '{branch_output}'", style="mom.warning"
            )
            if minutes_passed > 1440:
                console.print(
                    "This branch feels abandoned. Like your New Year’s goals.",
                    style="mom.italic",
                )
    except subprocess.CalledProcessError:
        console.print("❌ Failed to determine current branch.", style="mom.error")

    try:
        status_output = subprocess.check_output(
            ["git", "status", "--porcelain"], text=True
        )
        dirty = bool(status_output.strip())
    except subprocess.CalledProcessError:
        console.print("❌ Failed to check git status.", style="mom.error")
        return

    if minutes_passed < 60:
        console.print(
            f"🕒 Last commit was {minutes_passed} minutes ago.", style="mom.info"
        )
        console.print("Not bad. But don't get cocky.", style="mom.italic")
    elif minutes_passed < 180:
        console.print(
            f"⏱️ It's been {minutes_passed // 60} hours since your last commit.",
            style="mom.warning",
        )
        console.print(
            "Maybe it’s time to save your progress, genius.", style="mom.italic"
        )
    elif minutes_passed < 1440:
        console.print(
            f"🚨 It’s been {minutes_passed // 60} hours since you last committed!",
            style="mom.error",
        )
        console.print("You said it would be quick. Liar.", style="mom.italic")
    else:
        days = minutes_passed // 1440
        console.print(
            f"💀 It’s been {days} day(s) since your last commit.", style="mom.error"
        )
        console.print(
            "Do you even remember what you were working on?", style="mom.italic"
        )
        console.print("Your code is gathering dust. Literally.", style="mom.italic")

    if dirty:
        console.print("\n🧼 You have uncommitted changes.", style="mom.warning")
        console.print(
            "What if your laptop explodes? Think about that.", style="mom.italic"
        )
        num_changes = len(status_output.strip().splitlines())
        console.print(
            f"{num_changes} things left behind. Like your chores.", style="mom.warning"
        )

    console.print("\n✅ mom nag completed. Your guilt is noted.", style="mom.info")
