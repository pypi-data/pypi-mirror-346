"""Command-line interface."""

import os

import click

from ssb_pubmd.browser_context import BrowserRequestContext as RequestContext
from ssb_pubmd.markdown_syncer import MarkdownSyncer


@click.group()
def cli() -> None:
    """Command-line interface for the ssb_pubmd package."""
    pass


@click.command()
def login() -> None:
    """Login to the server."""
    login_url = os.getenv("PUBMD_LOGIN_URL", "")
    request_context = RequestContext()
    print(login_url)
    storage_state_file, storage_state = request_context.create_new(login_url)
    click.echo(
        f"The following browser context object is now stored in {storage_state_file}:"
    )
    click.echo(storage_state)


@click.command()
@click.argument("content_file_path", type=click.Path())
def sync(content_file_path: str) -> None:
    """Sync the content."""
    post_url = os.getenv("PUBMD_POST_URL", "")
    request_context = RequestContext()
    request_context.recreate_from_file()

    syncer = MarkdownSyncer(post_url=post_url, request_context=request_context)
    syncer.content_file_path = content_file_path

    content_id = syncer.sync_content()

    click.echo(
        f"File '{click.format_filename(content_file_path)}' synced to CMS with content ID: {content_id}"
    )


cli.add_command(login)
cli.add_command(sync)

if __name__ == "__main__":
    cli()  # pragma: no cover
