from ape import plugins


@plugins.register(plugins.Config)
def config_class():
    from .ecosystem import OORTConfig

    return OORTConfig


@plugins.register(plugins.EcosystemPlugin)
def ecosystems():
    from .ecosystem import OORT

    yield OORT


@plugins.register(plugins.NetworkPlugin)
def networks():
    from ape.api.networks import (
        LOCAL_NETWORK_NAME,
        ForkedNetworkAPI,
        NetworkAPI,
        create_network_type,
    )

    from .ecosystem import NETWORKS

    for network_name, network_params in NETWORKS.items():
        yield "oort", network_name, create_network_type(*network_params)
        yield "oort", f"{network_name}-fork", ForkedNetworkAPI

    # NOTE: This works for development providers, as they get chain_id from themselves
    yield "oort", LOCAL_NETWORK_NAME, NetworkAPI


@plugins.register(plugins.ProviderPlugin)
def providers():
    from ape.api.networks import LOCAL_NETWORK_NAME
    from ape_node import Node
    from ape_test import LocalProvider

    from .ecosystem import NETWORKS

    for network_name in NETWORKS:
        yield "oort", network_name, Node

    yield "oort", LOCAL_NETWORK_NAME, LocalProvider


def __getattr__(name: str):
    if name == "NETWORKS":
        from .ecosystem import NETWORKS

        return NETWORKS

    elif name == "OORT":
        from .ecosystem import OORT

        return OORT

    elif name == "OORTConfig":
        from .ecosystem import OORTConfig

        return OORTConfig

    else:
        raise AttributeError(name)


__all__ = [
    "NETWORKS",
    "OORT",
    "OORTConfig",
]
