from enum import StrEnum

from .ldap import Person


class Formats(StrEnum):
    """predifined output formats"""

    email = "email"
    fedid = "fedid"
    ansible = "ansible"
    csv = "csv"
    raw = "raw"


def format_results(
    results: list[Person], format: Formats = Formats.email, format_str: str = ""
) -> None:
    """
    Format the results of the LDAP query.
    """

    for user in sorted(results):
        # using match allows us to use fstring features not available to str.format()
        if format_str:
            try:
                output = format_str.format(user=user)
            except KeyError:
                print("format_str should contain fields like: '{user.cn}'")
                exit(1)
        else:
            match format:
                case Formats.ansible:
                    output = (
                        f"- {user.cn:12} # {user.sn + ', ' + user.givenName:28}"
                        f"  {user.mail}"
                    )
                case Formats.email:
                    output = f"{user.mail}"
                case Formats.fedid:
                    output = f"{user.cn}"
                case Formats.csv:
                    output = f'{user.cn}, "{user.displayName}", {user.mail}'
                case Formats.raw:
                    output = str(user)

        # skip blank format results
        if output != "":
            print(output)
