// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;


import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC721/ERC721.sol";
/* import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC721/extensions/IERC721Metadata.sol"; */

import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/utils/Counters.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/security/ReentrancyGuard.sol";



contract IrlVault is ERC721 {
  using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    constructor() ERC721("MyNFT", "MNFT") {
    }

    function mintNft() public returns (uint256){
      uint256 newTokenId = _tokenIds.current();
      _safeMint(msg.sender, newTokenId);
      _tokenIds.increment();
      return newTokenId;
    }


}
