import click
import subprocess
import json
import os
from mom.utils.style import console


@click.command()
def cover():
    """Check test coverage like mom would."""
    console.print("mom is checking your test coverage... ☂️", style="mom.info")

    if not os.path.exists(".coverage") or not os.path.exists("coverage.json"):
        console.print("⚠️ No recent coverage data found.", style="mom.warning")
        answer = (
            input("Do you want mom to run your tests for you with coverage? (Y/n) ")
            .strip()
            .lower()
        )
        if answer in ["", "y", "yes"]:
            try:
                console.print("Running tests with coverage... 🧪", style="mom.info")
                subprocess.run(
                    ["coverage", "run", "--source=.", "-m", "pytest"], check=True
                )
            except subprocess.CalledProcessError:
                console.print(
                    "❌ Tests failed or could not be run with coverage.",
                    style="mom.error",
                )
                return
        else:
            if not os.path.exists("coverage.json"):
                console.print(
                    "🚫 No coverage data available. Mom can’t work with nothing.",
                    style="mom.error",
                )
                return
            console.print(
                "⚠️ Using potentially outdated coverage data. Mom is not responsible for this mess.",
                style="mom.warning",
            )

    try:
        with open("coverage.json", "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        console.print("❌ Failed to parse coverage output.", style="mom.error")
        return

    console.print("📊 Coverage data loaded.", style="mom.success")

    totals = data.get("totals", {})
    percent = totals.get("percent_covered", 0)

    console.print(f"\n💯 Total coverage: {percent:.1f}%", style="mom.bold")

    if percent >= 90:
        console.print("You're amazing. Mom is crying. 😭", style="mom.success")
    elif percent >= 75:
        console.print(
            "Not bad, sweetheart. But you can do better. 💁", style="mom.info"
        )
    else:
        console.print("I'm not angry. Just disappointed. 💔", style="mom.error")

    console.print("\n📁 Files with low coverage:", style="mom.underline")
    for file, file_percent in get_low_coverage_files():
        console.print(f"✗ {file} → {file_percent:.1f}%", style="mom.warning")


def get_low_coverage_files(threshold=80):
    if not os.path.exists("coverage.json"):
        return []

    try:
        with open("coverage.json", "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return []

    low_files = []
    for file, file_data in data.get("files", {}).items():
        file_percent = file_data.get("summary", {}).get("percent_covered", 100)
        if file_percent < threshold:
            low_files.append((file, file_percent))

    return low_files
