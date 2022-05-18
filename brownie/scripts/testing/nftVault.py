import os
from brownie import SimpleNft, SimpleNftDeposit, accounts, network, config, web3

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

def createNft():
    transaction = SimpleNft.deploy( {"from":devAccount, "gas_price": gas_strategy, "allow_revert":revert}, publish_source=publishSource)
    nft = transaction
    print(f"nft deploy at {transaction.address} ")
    return nft

def mintNft(_contract):
    _erc721 = _contract
    _tokenId = _erc721.mintNft({"from":devAccount}).return_value
    print(f"token id {_tokenId}")
    return _tokenId

def transferFunds(_contract,_from, _to, _tokenId):
    _erc721 = _contract
    _erc721.safeTransferFrom(_from, _to, _tokenId, {"from":devAccount})
    # _erc721.safeTransferFrom(bob, 100, {"from":devAccount})
    # print(f"Alice balance {_erc721.balanceOf(alice)}")
    # print(f"Bob balance {_erc721.balanceOf(bob)}")


def createVault():
    transaction = SimpleNftDeposit.deploy( {"from":devAccount, "gas_price": gas_strategy, "allow_revert":revert}, publish_source=publishSource)
    return transaction

def approveVault(_token, _vault, _user, _tokenId):
    _token.approve(_vault.address, _tokenId, {'from': _user})



def depositTokens(_vault, _nftAddress, _tokenId, _user):
    # address _nftAddress,uint256 _tokenId
    _vault.depositNft(_nftAddress, _tokenId, {'from': _user})

def withdrawTokens(_vault, _nftAddress, _tokenId, _user):
    # address _nftAddress, uint256 _tokenId
    _vault.withdrawNft(_nftAddress, _tokenId, {'from': _user})


def main():
    nftToken = createNft()
    _token1 = mintNft(nftToken)
    _token2 = mintNft(nftToken)
    _token3 = mintNft(nftToken)
    print(f"Alice balance {nftToken.balanceOf(alice)}")
    print(f"Bob balance {nftToken.balanceOf(bob)}")
    transferFunds(nftToken, devAccount, alice, _token1)
    transferFunds(nftToken, devAccount, bob, _token2)
    transferFunds(nftToken, devAccount, alice, _token3)
    print(f"Alice balance {nftToken.balanceOf(alice)}")
    print(f"Bob balance {nftToken.balanceOf(bob)}")
    # transaction = HelloToken.deploy(initialSupply, {"from":devAccount, "gas_price": gas_strategy, "allow_revert":revert}, publish_source=publishSource)
    print(nftToken.address)
    vault = createVault()
    print(f"Balance of alice : {nftToken.balanceOf(alice)}")
    approveVault(nftToken,vault,alice, _token1)
    depositTokens(vault,nftToken.address,_token1, alice)
    print(f"Balance of alice : {nftToken.balanceOf(alice)}")
    withdrawTokens(vault,nftToken.address,_token1, alice)
    print(f"Balance of alice : {nftToken.balanceOf(alice)}")
    approveVault(nftToken,vault,alice, _token3)
    depositTokens(vault,nftToken.address,_token3, alice)
    # delegate = vault.getDelegatedOwner(nftToken.address,0).return_value
    # print(f"delegate for 0 token : {delegate}")
    delegate = vault.updateDelegatedAddress(nftToken.address,2, accounts[5], {"from":alice}).return_value
    print(f"delegate for 0 token : {delegate}")
    delegate = vault.getDelegatedOwner(nftToken.address,2, {"from":alice}).return_value
    print(f"delegate for 0 token : {delegate}")
