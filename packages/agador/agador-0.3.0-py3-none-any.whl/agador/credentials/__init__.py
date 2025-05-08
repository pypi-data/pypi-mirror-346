from ..loaders import parse_credential_map
from nornir.core import Nornir
from nornir.core.inventory import ConnectionOptions


def resolve_credentials(cred_map, cfg):
    """
    Resolving all credentials in the cred map based on their
    mapper functions
    """

    # first we need to resolve all the credentials in the map
    _resolve_cred(cred_map["defaults"], cfg)
    for custom_cred in cred_map["custom"]:
        _resolve_cred(custom_cred, cfg)


def _resolve_cred(cred, cfg):
    """
    Resolves enable and password fields in the credential map using the specified mapper
    """
    pw_keys = ["password", "enable"]
    for key in pw_keys:
        if key in cred:
            cred[key] = cred["mapper"](cred[key], cfg)

def update_nornir_credentials(nr: Nornir, cfg: dict):
    """
    Uses the credential map to update host credentials in this nornir instance
    """

    # parse and resolve credentials
    cred_map = parse_credential_map(cfg)
    resolve_credentials(cred_map, cfg)

    # set nornir default username and password
    nr.inventory.defaults.username = cred_map["defaults"]["username"]
    nr.inventory.defaults.password = cred_map["defaults"]["password"]
    if cred_map["defaults"]["enable"]:
        conn_options = ConnectionOptions(
            extras={"optional_args": {"secret": cred_map["defaults"]["enable"]}}
        )
        nr.inventory.defaults.connection_options["umnet_napalm"] = conn_options

    # for each host in the inventory, if there's a custom
    # match, set the credentials for that host
    for host in nr.inventory.hosts.values():

        # we only want to match a custom credential once for a particular host
        # the first match on the list
        found_custom_cred = False

        for custom_cred in cred_map["custom"]:
            if custom_cred["inventory_filter"](host) and not found_custom_cred:

                found_custom_cred = True
                host.username = custom_cred["username"]
                host.password = custom_cred["password"]

                if custom_cred.get("enable"):
                    conn_options = ConnectionOptions(
                        extras={"optional_args": {"secret": custom_cred["enable"]}}
                    )
                    host.connection_options["umnet_napalm"] = conn_options
