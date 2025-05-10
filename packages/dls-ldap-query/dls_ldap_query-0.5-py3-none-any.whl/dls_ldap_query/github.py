"""
A function to extract the list of fedids of GitHub users currently registered
in the gitlab repo https://gitlab.diamond.ac.uk/github/github-members
"""

import os
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

REPO = "https://gitlab.diamond.ac.uk/github/github-members"


def get_github_members() -> list[str]:
    """Look in github members repo and generate a list of fedids"""
    folder = Path(mkdtemp())
    os.system(f"git clone {REPO} {folder} &> /dev/null")

    member_fedids = []

    user_files = (folder / "users").glob("*.yaml")
    for name in user_files:
        member_fedids.append(name.stem)

    rmtree(folder)
    return member_fedids
