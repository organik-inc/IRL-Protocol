import os
from brownie import SimpleNft, accounts, network, config, web3

from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

gas_price(gas_strategy)


# nft.mintNft({'from':accounts[0], "gas_price": gas_strategy})
nft = SimpleNft.at("0x254dffcd3277C0b1660F6d42EFbB754edaBAbC2B")

nft.mintNft({'from':accounts[0], "gas_price": gas_strategy})


def main():
    devAccount = accounts.add(config["wallets"]["devKey"])
    print(f"current network {network.show_active()}")
    publishSource = True if os.getenv("ETHERSCAN_TOKEN") else False
    if network.show_active() == "development":
        publishSource = False
    if network.show_active() == "maticRPC":
        publish_source = True
        revert = False
    else:
        revert = True
    if revert is None:
        revert = False
    transaction = SimpleNft.deploy( {"from":devAccount, "gas_price": gas_strategy, "allow_revert":revert}, publish_source=publishSource)
    print(transaction)
