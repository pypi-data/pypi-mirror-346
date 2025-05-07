import click
from mom.utils.style import console
from mom.commands.status import get_status_summary
from mom.commands.cover import get_low_coverage_files
from mom.commands.tidy import check_tidy_problems
from mom.commands.plan import get_plan_age_minutes


@click.command()
def suggest():
    """mom looks at your project and tells you what to do. With love."""

    console.print("mom is thinking... 🧠\n", style="mom.info")

    uncommitted, minutes = get_status_summary()
    if uncommitted:
        console.print("🧼 You have uncommitted changes.", style="mom.warning")
        console.print(
            "You should commit, genius. That’s what Git is for.\n", style="mom.dim"
        )

    if minutes is None:
        console.print(
            "⏱️ Couldn’t check commit time. Are you even in a git repo?",
            style="mom.error",
        )
    elif minutes > 60:
        console.print(
            f"⏱️ Last commit was {minutes} minute(s) ago.", style="mom.warning"
        )
        console.print(
            "Maybe it’s time to save your progress. Just saying.\n", style="mom.dim"
        )

    low_coverage = get_low_coverage_files()
    if low_coverage:
        console.print("☂️ Some files are poorly tested:", style="mom.warning")
        for file, percent in low_coverage:
            console.print(f"✗ {file} → {percent:.1f}%", style="mom.italic")
        console.print(
            "These files are embarrassing. Do your tests even lift?\n", style="mom.dim"
        )

    tidy_results = check_tidy_problems()
    if any(result != "success" for result in tidy_results.values()):
        console.print("🧹 Code could use a cleanup.", style="mom.warning")
        for tool, result in tidy_results.items():
            if result != "success":
                console.print(f"• {tool} returned issues.", style="mom.italic")
        console.print("Want mom to fix it for you?\n", style="mom.dim")

    plan_age = get_plan_age_minutes()
    if plan_age is None:
        console.print("🧠 No current plan found.", style="mom.warning")
        console.print(
            "Did you even tell me what you’re working on today?\n", style="mom.dim"
        )
    elif plan_age > 480:
        console.print(
            f"📅 Your plan is {plan_age // 60} hour(s) old.", style="mom.warning"
        )
        console.print("Is it still valid or were you just dreaming?\n", style="mom.dim")

    console.print("\n📋 Summary:", style="mom.info")
    console.print(f"{'✓' if not uncommitted else '✗'} Commit state", style="mom.dim")
    console.print(f"{'✓' if not low_coverage else '✗'} Test coverage", style="mom.dim")
    tidy_issue = any(result != "success" for result in tidy_results.values())
    console.print(f"{'✓' if not tidy_issue else '✗'} Code style", style="mom.dim")
    if plan_age is None or plan_age > 480:
        console.print("✗ Active plan", style="mom.dim")
    else:
        console.print("✓ Active plan", style="mom.dim")

    console.print(
        "✅ mom suggest completed. Whether you listen is another matter.\n",
        style="mom.success",
    )
