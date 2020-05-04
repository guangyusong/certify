var Purchase = artifacts.require("./Purchase.sol");
var Activate = artifacts.require("./Activate.sol");

module.exports = function (deployer) {
    deployer.deploy(Purchase).then(function () {
        return deployer.deploy(Activate, Purchase.address);
    })
};