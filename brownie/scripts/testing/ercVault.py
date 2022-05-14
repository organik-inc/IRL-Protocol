import os
from brownie import HelloToken, SimpleDeposit, accounts, network, config, web3

from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

gas_price(gas_strategy)

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

# test accounts
alice = accounts[1]
bob = accounts[2]

def createErc20():
    initialSupply = 1000000000000000000000
    transaction = HelloToken.deploy(initialSupply, {"from":devAccount, "gas_price": gas_strategy, "allow_revert":revert}, publish_source=publishSource)
    erc20 = transaction
    print(f"erc20 deploy at {transaction.address} ")
    return erc20

def transferFunds(_contract):
    _erc20 = _contract
    _erc20.transfer(alice, 100, {"from":devAccount})
    _erc20.transfer(bob, 100, {"from":devAccount})
    print(f"Alice balance {_erc20.balanceOf(alice)}")
    print(f"Bob balance {_erc20.balanceOf(bob)}")


def createVault(_tokenAddress):
    transaction = SimpleDeposit.deploy(_tokenAddress, {"from":devAccount, "gas_price": gas_strategy, "allow_revert":revert}, publish_source=publishSource)
    return transaction

def approveVault(_token, _vault, _user, _amount):
    _token.approve(_vault.address, _amount, {'from': _user})



def depositTokens(_vault, _user,_amount):
    _vault.stake(_amount, {'from': _user})

def withdrawTokens(_vault, _user, _amount):
    _vault.withdraw(_amount, {'from': _user})


def main():
    erc20Token = createErc20()
    transferFunds(erc20Token)
    # transaction = HelloToken.deploy(initialSupply, {"from":devAccount, "gas_price": gas_strategy, "allow_revert":revert}, publish_source=publishSource)
    print(erc20Token.address)
    vault = createVault(erc20Token.address)
    print(f"Balance of alice : {erc20Token.balanceOf(alice)}")
    approveVault(erc20Token,vault,alice, 100)
    depositTokens(vault,alice,20)
    print(f"Balance of alice : {erc20Token.balanceOf(alice)}")
    withdrawTokens(vault,alice,10)
    print(f"Balance of alice : {erc20Token.balanceOf(alice)}")
