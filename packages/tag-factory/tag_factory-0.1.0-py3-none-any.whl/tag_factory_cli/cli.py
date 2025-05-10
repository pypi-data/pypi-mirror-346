"""
Tag Factory CLI tool main entry point.
"""
import click

from tag_factory_cli import __version__
from tag_factory_cli.tags import TagManager
from tag_factory_cli.workspaces import WorkspaceManager


@click.group()
@click.version_option(version=__version__)
def cli():
    """Tag Factory CLI tool."""
    pass


@cli.command()
def hello():
    """Simple command to test the CLI."""
    click.echo("Hello from Tag Factory CLI!")


@cli.group()
def tags():
    """Commands for managing tags."""
    pass


@tags.command()
@click.option("--workspace", required=True, help="Workspace ID")
def list(workspace):
    """List all tags in a workspace."""
    try:
        tag_manager = TagManager()
        tags = tag_manager.list_tags(workspace)
        click.echo(f"Tags in workspace {workspace}:")
        for tag in tags:
            click.echo(f"- {tag['name']}: {tag.get('description', 'No description')}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@cli.group()
def workspaces():
    """Commands for managing workspaces."""
    pass


@workspaces.command("list")
def list_workspaces():
    """List all workspaces."""
    try:
        workspace_manager = WorkspaceManager()
        workspaces = workspace_manager.list_workspaces()
        print(f"Total workspaces: {len(workspaces)}")
        click.echo("Available workspaces:")
        for workspace in workspaces:
            click.echo(f"- {workspace['name']} (ID: {workspace['id']})")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@workspaces.command()
@click.argument("id")
def get(id):
    """Get workspace details."""
    try:
        workspace_manager = WorkspaceManager()
        workspace = workspace_manager.get_workspace(id)
        click.echo(f"Workspace: {workspace['name']}")
        click.echo(f"ID: {workspace['id']}")
        click.echo(f"Description: {workspace.get('description', 'No description')}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
