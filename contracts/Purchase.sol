pragma solidity ^0.5.0;


// The main contract responsible for purchasing and activating the product
contract Purchase {
    // Struct recording the transaction and activation details
    struct Transaction {
        string customer;
        uint256 price;
        string key; // Used to store the block hash later for storage purposes
        bool activated;
    }

    // Array of transactions
    Transaction[] public listOfTransactions;

    // The transaction number
    uint256 lastTransactionId = 0;

    // Event with the last transaction Id. This is emitted after a transaction.
    event transactionEvent(uint256 _id);

    // Purchasing a product
    function purchase(
        uint256 productId,
        uint256 productCost,
        string memory account
    ) public payable returns (uint256) {
        // Record Transaction Details
        Transaction memory newTransaction;
        newTransaction.customer = account;
        newTransaction.price = productCost;
        newTransaction.activated = false;

        // Add new transaction to array
        listOfTransactions.push(newTransaction);

        // Emit event with sale ID
        emit transactionEvent(lastTransactionId);

        // Increment sale ID
        lastTransactionId += 1;

        // Return productId
        return productId;
    }

    // Get the license's activation status
    function getLicenseStatus(uint256 id) public view returns (bool) {
        return listOfTransactions[id].activated;
    }

    // Set the license's activation status
    function setLicenseStatus(uint256 id) public {
        listOfTransactions[id].activated = true;
    }

    // Register the license key under the customer
    function storeLicense(uint256 id, string memory blockHash) public {
        listOfTransactions[id].key = blockHash;
    }
}
