// SPDX-License-Identifier: MIT
// Inspired by https://solidity-by-example.org/defi/staking-rewards/
//this version is taken from https://raw.githubusercontent.com/smartcontractkit/defi-minimal/main/contracts/Staking.sol and modified
pragma solidity ^0.8.7;


import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/security/ReentrancyGuard.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC20/IERC20.sol";
/* import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC20/ERC20.sol"; */
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC721/IERC721Receiver.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC721/extensions/IERC721Metadata.sol";


error TransferFailed();
error NeedsMoreThanZero();

/* example of double mapping
https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.5.0/contracts/token/ERC20/ERC20.sol#L38
mapping(address => mapping(address => uint256)) private _allowances;
_allowances[owner][spender] = amount;
_allowances[owner][spender];
 */

contract SimpleNftDeposit is ReentrancyGuard {
  IERC721Metadata public depositedNft;

  struct nftDelegate{
    bool enabled;
    uint depositBlock;
    address delegate;
    address depositOwner;

  }


  /* _owners[collection][id]; */
  /* mapping(address => mapping(uint256 => mapping(address => nftDelegate))) private _owners; */
  mapping(address => mapping(uint256 => nftDelegate)) private _owners;


  /* mapping(address => uint256) public owner; */


  constructor(){

  }

  function depositNft(address _nftAddress,uint256 _tokenId) external nonReentrant {
    depositedNft = IERC721Metadata(_nftAddress);
    address owner = depositedNft.ownerOf(_tokenId);
    require(owner != address(0), "Deposit from the zero address");
    require(owner == msg.sender, "Deposit not from owner");


    _owners[_nftAddress][_tokenId] = nftDelegate({
      enabled: true,
      depositBlock: block.number,
      delegate: address(0),
      depositOwner: msg.sender
      });

      depositedNft.safeTransferFrom(msg.sender, address(this), _tokenId);



    /* _owners[_nftAddress][_tokenId][msg.sender] */

  }

  function ownerOf(address _nftAddress, uint256 _tokenId ) public returns(address) {
    /* depositedNft = IERC721Metadata(_nftAddress); */
    address depositOwner = _owners[_nftAddress][_tokenId].depositOwner;
    return depositOwner;

  }

  function withdrawNft(address _nftAddress, uint256 _tokenId) external deleteDelegate(_nftAddress, _tokenId)  {
     depositedNft = IERC721Metadata(_nftAddress);
     /* address owner = depositedNft.ownerOf(_tokenId); */
     address owner = ownerOf(_nftAddress, _tokenId);
     require(owner != address(0), "Withdraw to the zero address");
     require(owner == msg.sender, "Withdraw not from owner");
     depositedNft.safeTransferFrom(address(this), msg.sender, _tokenId);



  }

/*
Modifier Functions
 */
 modifier deleteDelegate(address _nftAddress, uint256 _tokenId){
     _;
   delete(
     _owners[_nftAddress][_tokenId]
     );
 }

 modifier onlyStakedOwner(address _nftAddress, uint256 _tokenId){
   depositedNft = IERC721Metadata(_nftAddress);
   address owner = depositedNft.ownerOf(_tokenId);

   _;

 }

}
