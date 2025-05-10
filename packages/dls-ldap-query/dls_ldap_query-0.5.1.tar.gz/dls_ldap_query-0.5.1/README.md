[![CI](https://github.com/DiamondLightSource/dls-ldap-query/actions/workflows/ci.yml/badge.svg)](https://github.com/DiamondLightSource/dls-ldap-query/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/DiamondLightSource/dls-ldap-query/branch/main/graph/badge.svg)](https://codecov.io/gh/DiamondLightSource/dls-ldap-query)
[![PyPI](https://img.shields.io/pypi/v/dls-ldap-query.svg)](https://pypi.org/project/dls-ldap-query)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# dls_ldap_query

Format lists of users by querying LDAP

Source          | <https://github.com/DiamondLightSource/dls-ldap-query>
:---:           | :---:
PyPI            | `pip install dls-ldap-query`
Docker          | `docker run ghcr.io/diamondlightsource/dls-ldap-query:latest`
Releases        | <https://github.com/DiamondLightSource/dls-ldap-query/releases>

The following command gives details of the command line parameters:

```
dls_ldap_query --help
```
## Temporary deployment

This will be deployed as an environment module. But for the moment you can access it at DLS using this path:
```
/dls_sw/work/python3/dls-ldap-query --help
```

## Example Usage

Get the email addresses of everyone in group `dcs`
```bash
dls-ldap-query --group dcs
```

Get the fedids of all the users in GitHub Members.
(this requires access to the github-members GitLab repository)
```bash
dls-ldap-query --repo --output fedid
```

Get the fedids of all the users in `Diamond Beamline Controls` Outlook distribution list.
- Click `New Email` in outlook and start typing the DL name, hit enter once the correct DL is highlighted
- Click on the + to the left of the DL name - this expands it into its members
- Ctrl-A Ctrl-C (select all names and copy to clipboard)
- paste these names into a file e.g. /tmp/names.txt and save it
```bash
dls-ldap-query --email --file /tmp/names.txt
# OR
dls-ldap-query --email '"Knap, Giles (DLSLtd,RAL,LSCI)" <giles.knap@diamond.ac.uk>; "Cob ... '
```
NOTE: you can paste the email members directly to the command line but you must enclose them in single quotes and remove any apostrophes in names! (which is why the file approach is easier)
