import click
from mom.commands import status, tidy, cover, nag, plan, focus, suggest


@click.group()
def cli():
    """mom — your codebase’s emotional support CLI"""
    pass


cli.add_command(status.status)
cli.add_command(tidy.tidy)
cli.add_command(cover.cover)
cli.add_command(nag.nag)
cli.add_command(plan.plan)
cli.add_command(focus.focus)
cli.add_command(suggest.suggest)

if __name__ == "__main__":
    cli()
