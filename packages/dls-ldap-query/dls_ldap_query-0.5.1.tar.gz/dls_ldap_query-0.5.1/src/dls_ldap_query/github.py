"""
A function to extract the list of fedids of GitHub users currently registered
in the gitlab repo https://gitlab.diamond.ac.uk/github/github-members
"""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

REPO = "https://gitlab.diamond.ac.uk/github/github-members"


def get_github_members() -> list[str]:
    """Look in github members repo and generate a list of fedids"""

    with TemporaryDirectory() as tmp:
        tmp_folder = Path(tmp)
        os.system(f"git clone {REPO} {tmp_folder} &> /dev/null")

        member_fedids = []

        user_files = (tmp_folder / "users").glob("*.yaml")
        for name in user_files:
            member_fedids.append(name.stem)

        return member_fedids
