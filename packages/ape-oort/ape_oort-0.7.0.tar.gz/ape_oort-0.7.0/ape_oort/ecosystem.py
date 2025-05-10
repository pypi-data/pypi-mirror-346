from typing import ClassVar, cast

from ape_ethereum.ecosystem import (
    BaseEthereumConfig,
    Ethereum,
    NetworkConfig,
    create_network_config,
)

NETWORKS = {
    # chain_id, network_id
    "mainnet": (970, 970),
    "testnet": (9700, 9700),
    "local": (9900, 9900),
}


class OORTConfig(BaseEthereumConfig):
    NETWORKS: ClassVar[dict[str, tuple[int, int]]] = NETWORKS
    mainnet: NetworkConfig = create_network_config(
        block_time=0, required_confirmations=0, is_mainnet=True
    )
    testnet: NetworkConfig = create_network_config(block_time=0, required_confirmations=0)
    local: NetworkConfig = create_network_config(block_time=0, required_confirmations=0)


class OORT(Ethereum):
    fee_token_symbol: str = "OORT"

    @property
    def config(self) -> OORTConfig:  # type: ignore[override]
        return cast(OORTConfig, self.config_manager.get_config("oort"))
