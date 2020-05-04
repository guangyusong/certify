pragma solidity ^0.5.0;

import "./Purchase.sol";


contract Activate {
    // Initialize an instance of the Purchase Contract
    Purchase purchase;

    // Constructor
    constructor(address _purchase) public {
        purchase = Purchase(_purchase);
    }

    // Check if product is activated
    function isActive(uint256 saleId) public returns (bool) {
        return purchase.getLicenseStatus(saleId);
    }

    // Activate product
    function activateProduct(uint256 saleId, string memory blockHash) public {
        // The product must not activated
        require(false == isActive(saleId), "License is already active");

        // Activate the ID, and store the block hash of the purchase
        // on the server side so we know exactly which product was activated
        purchase.setLicenseStatus(saleId);
        purchase.storeLicense(saleId, blockHash);
    }
}
