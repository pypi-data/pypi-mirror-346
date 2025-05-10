"""Interface for ``python -m dls_ldap_query``."""

import grp
import re
from pathlib import Path
from typing import Annotated

import typer

from . import __version__
from .formatter import Formats, format_results
from .github import get_github_members
from .ldap import ATTRIBUTES, LDAPServer

__all__ = ["main"]

RE_EMAIL = re.compile(r"\<([^\>]*)\>")


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


def main():
    """
    Main entry point for this module - dls_ldap_query.
    """
    typer.run(query)


def query(
    search_string: Annotated[
        str, typer.Argument(help="A comma separaed list of search terms.")
    ] = "",
    output: Annotated[
        Formats,
        typer.Option("--output", "-o", help="Predefined formats for the output."),
    ] = Formats.email,
    format_str: Annotated[
        str,
        typer.Option(
            "--format_str",
            "-x",
            help="Supply a custom format string enclosed in single quotes."
            "e.g. '{user.givenName} {user.sn} {user.mail}'",
        ),
    ] = "",
    group: Annotated[
        str | None,
        typer.Option(
            "--group", "-g", help="A linux group name to extract user ids from."
        ),
    ] = None,
    file: Annotated[
        Path | None,
        typer.Option(
            "-f",
            "--file",
            help="Supply the search terms in a file. Line break separated.",
        ),
    ] = None,
    repo: Annotated[
        bool,
        typer.Option(
            "-r",
            "--repo",
            help="Get the list of fedids from the github-members GitLab repository.",
        ),
    ] = False,
    email: Annotated[
        bool,
        typer.Option(
            "--email",
            "-e",
            help="A flag that treats the search string as a list of emails"
            " copied from Outlook.",
        ),
    ] = False,
    attribute: Annotated[
        str,
        typer.Option(
            "--attribute",
            "-a",
            help=f"The LDAP attribute to search for "
            f"(cn=common_name=fedID): {list(ATTRIBUTES)}",
        ),
    ] = "cn",
    server: Annotated[
        str,
        typer.Option(
            "--server",
            "-s",
            help="The LDAP server to connect to.",
        ),
    ] = LDAPServer.default_server_url,
    search_base: Annotated[
        str,
        typer.Option(
            "-b",
            help="The LDAP search base to use.",
        ),
    ] = LDAPServer.default_search_base,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            help="Print the version number and exit",
        ),
    ] = None,
):
    # alternative sources of search_string
    if group:
        # search for all users in a linux group
        group_obj = grp.getgrnam(group)
        attribute = "cn"  # searching by fedid
        search_array = group_obj.gr_mem
    elif file:
        search_string = file.read_text()
        search_array = search_string.splitlines()
    elif repo:
        search_array = get_github_members()
    else:
        # treat search_string as a comma separated list
        search_array = search_string.split(",")

    if email:
        # extract the emails from a list pasted from outlook
        search_array = RE_EMAIL.findall(search_string)
        attribute = "mail"  # searching by email address

    ldap_server = LDAPServer(server, search_base)

    entries = ldap_server.search(search_array, attribute)
    format_results(entries, format=output, format_str=format_str)


if __name__ == "__main__":
    typer.run(query)
