// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/* import "@openzeppelin/contracts/token/ERC20/ERC20.sol"; */
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC20/ERC20.sol";


contract HelloToken is ERC20 {
    // wei
    constructor(uint256 initialSupply) ERC20("HelloToken", "HT") {
        _mint(msg.sender, initialSupply);
    }
}



contract InflationBond {
  //make a deposit
}
