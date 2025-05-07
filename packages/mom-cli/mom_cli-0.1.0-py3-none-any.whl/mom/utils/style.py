from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "mom.info": "bold cyan",
        "mom.success": "green",
        "mom.warning": "yellow",
        "mom.error": "bold red",
        "mom.italic": "italic",
        "mom.bold": "bold",
        "mom.underline": "underline",
        "mom.dim": "dim",
    }
)

console = Console(theme=custom_theme)
