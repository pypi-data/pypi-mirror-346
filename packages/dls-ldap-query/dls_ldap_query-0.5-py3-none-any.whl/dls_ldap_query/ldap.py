from dataclasses import dataclass

import ldap3


# LDAP attributes to get. Full list that could be added herer is found at:
# https://www.ibm.com/docs/en/cip?topic=api-user-identity-attributes
@dataclass(order=True)
class Person:
    sn: str  # The surname of the person
    cn: str  # The common name (fedID)
    displayName: str  # e.g. Knap, Giles (DLSLtd,RAL,LSCI)
    mail: str  # The email address of the person
    givenName: str  # The first name of the person

    def __post_init__(self):
        # sort by surname (sn needs to be first in the attribute list above)
        self.sort_index = self.sn


# a list of the above fields
ATTRIBUTES = Person.__annotations__.keys()


class LDAPServer:
    default_server_url: str = "ralfed.cclrc.ac.uk"
    default_search_base: str = "ou=DLS,dc=fed,dc=cclrc,dc=ac,dc=uk"

    def __init__(self, server_url: str, search_base: str):
        self.server_url = server_url
        self.search_base = search_base
        self.server = ldap3.Server(server_url)
        self.connection = ldap3.Connection(self.server)
        self.connection.bind()

    def search(self, search_strings: list[str], attribute: str) -> list[Person]:
        result = []
        for search_string in search_strings:
            search_filter = f"({attribute}={search_string})"

            self.connection.search(
                search_base=self.search_base,
                search_filter=search_filter,
                attributes=ATTRIBUTES,
                search_scope=ldap3.SUBTREE,
            )

            for e in self.connection.entries:
                entry_dict = {}
                # flatten out the values into strings instead of lists of strings
                e_dict = e.entry_attributes_as_dict

                for key, value in e_dict.items():
                    if len(value) > 0:
                        entry_dict[key] = value[0]
                    else:
                        entry_dict[key] = ""
                if "cn" in entry_dict:
                    if entry_dict["cn"].lower() != entry_dict["cn"]:
                        # reject uppercase common name - not a fedid
                        continue
                else:
                    # reject entries that have no fedid
                    continue

                # convert to dataclass
                entry = Person(**entry_dict)
                result.append(entry)

        return result
