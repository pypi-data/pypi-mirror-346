import subprocess
import click
import shutil
from mom.utils.style import console
import sys
import os
import random


FINAL_MESSAGES = [
    "That's better. You're welcome. ❤️",
    "Mom’s proud. For now. 😌",
    "You can ship this. Maybe.",
    "I cleaned your mess again. You’re welcome.",
    "It’s not perfect, but at least it’s not shameful.",
    "I've seen worse. But not recently.",
]

REQUIRED_TOOLS = ["black", "ruff", "isort"]


def is_tool_installed(name):
    return shutil.which(name) is not None


def in_virtualenv():
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def prompt_install(tool_name):
    answer = (
        input(f"🔧 {tool_name} is missing. Want mom to install it for you? (Y/n) ")
        .strip()
        .lower()
    )
    return answer in ["", "y", "yes"]


# Helper to run a tool and print status
def run_tool(name, args):
    try:
        console.print(f"\n▶️ Running {name}...", style="mom.info")
        result = subprocess.run(args, capture_output=True, text=True)
        if result.stdout:
            console.print(result.stdout.strip(), style="mom.italic")
        if result.returncode == 0:
            console.print(f"✓ {name} completed successfully.", style="mom.success")
            return "success"
        else:
            console.print(f"⚠️ {name} returned errors:", style="mom.warning")
            console.print(result.stderr.strip(), style="mom.italic")
            return "warning"
    except Exception as e:
        console.print(f"❌ Failed to run {name}: {e}", style="mom.error")
        return "error"


@click.command()
def tidy():
    """Clean and format your codebase like mom would."""
    console.print("mom is cleaning your codebase. Sit tight. 🧹", style="mom.info")

    console.print("\n🧩 Checking for tools...", style="mom.info")

    tools = {}
    for tool in REQUIRED_TOOLS:
        if is_tool_installed(tool):
            console.print(f"✓ {tool} is installed", style="mom.success")
            tools[tool] = True
        else:
            if not in_virtualenv():
                console.print(
                    f"✗ {tool} is missing – and you’re not in a virtual environment!",
                    style="mom.error",
                )
                console.print(
                    "Please activate a virtual environment and try again. 👠",
                    style="mom.warning",
                )
                tools[tool] = False
                continue

            console.print(
                f"✗ {tool} is missing – how do you even live like this?",
                style="mom.error",
            )
            if prompt_install(tool):
                console.print(
                    f"Installing {tool} for you. Sit tight... 🛠️", style="mom.info"
                )
                try:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", tool], check=True
                    )
                    tools[tool] = True
                    console.print(
                        f"✓ {tool} installed successfully.", style="mom.success"
                    )
                except subprocess.CalledProcessError:
                    console.print(f"❌ Failed to install {tool}.", style="mom.error")
                    tools[tool] = False
            else:
                tools[tool] = False
                console.print(
                    f"❌ Skipped {tool} because you’re stubborn and refused to install it. Mom is not mad, just disappointed.",
                    style="mom.italic",
                )

    results = {}

    if tools.get("isort"):
        results["isort"] = run_tool("isort", ["isort", "."])
    if tools.get("black"):
        results["black"] = run_tool("black", ["black", "."])
    if tools.get("ruff"):
        results["ruff"] = run_tool("ruff", ["ruff", "check", ".", "--fix"])

    console.print("\n🧾 Summary:", style="mom.info")
    for tool, outcome in results.items():
        symbol = {"success": "✓", "warning": "⚠️", "error": "❌"}.get(outcome, "-")
        console.print(f"{symbol} {tool}: {outcome}", style="mom.italic")

    console.print(f"\n{random.choice(FINAL_MESSAGES)}", style="mom.italic")


def check_tidy_problems():
    """
    Returns a dict {tool_name: outcome} like {"black": "success", "ruff": "warning", ...}
    Only runs tools if they are installed. Skips installation logic.
    """
    results = {}
    for tool in REQUIRED_TOOLS:
        if is_tool_installed(tool):
            if tool == "isort":
                results["isort"] = run_tool("isort", ["isort", "."])
            elif tool == "black":
                results["black"] = run_tool("black", ["black", "."])
            elif tool == "ruff":
                results["ruff"] = run_tool("ruff", ["ruff", "check", ".", "--fix"])
    return results
