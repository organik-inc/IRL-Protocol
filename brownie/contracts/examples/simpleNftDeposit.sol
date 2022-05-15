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



contract SimpleNftDeposit is ReentrancyGuard {
  IERC721Metadata public depositedNft;

}
