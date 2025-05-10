import subprocess
import sys

from dls_ldap_query import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "dls_ldap_query", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
