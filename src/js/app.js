App = {
    web3Provider: null,
    contracts: {},

    init: async function () {
        // Load products.
        $.getJSON('../products.json', function (data) {
            var productRow = $('#productRow');
            var productTemplate = $('#productTemplate');

            for (i = 0; i < data.length; i++) {
                productTemplate.find('.panel-title').text(data[i].name);
                productTemplate.find('.panel-description').text(data[i].description);
                productTemplate.find('img').attr('src', data[i].picture);
                productTemplate.find('.old-price').text(data[i].old_price);
                productTemplate.find('.new-price').text(data[i].new_price);
                productTemplate.find('.btn-purchase').attr('data-id', data[i].id).attr('data-cost', data[i].cost);

                productRow.append(productTemplate.html());
            }
        });
        return await App.initWeb3();
    },

    initWeb3: async function () {
        // Modern dapp browsers...
        if (window.ethereum) {
            App.web3Provider = window.ethereum;
            try {
                // Request account access
                await window.ethereum.enable();
            } catch (error) {
                // User denied account access...
                console.error("User denied account access")
            }
        }
        // Legacy dapp browsers...
        else if (window.web3) {
            App.web3Provider = window.web3.currentProvider;
        }
        // If no injected web3 instance is detected, fall back to Ganache
        else {
            App.web3Provider = new Web3.providers.HttpProvider('http://localhost:7545');
        }
        web3 = new Web3(App.web3Provider);

        return App.initContract();
    },

    initContract: function () {
        $.getJSON('Purchase.json', function (data) {
            // Get the necessary contract artifact file and instantiate it with truffle-contract
            var PurchaseArtifact = data;
            App.contracts.Purchase = TruffleContract(PurchaseArtifact);

            // Set the provider for our contract
            App.contracts.Purchase.setProvider(App.web3Provider);
        });

        return App.bindEvents();
    },

    bindEvents: function () {
        $(document).on('click', '.btn-purchase', App.handlePurchase);
    },

    handlePurchase: function (event) {
        event.preventDefault();

        // Get product ID
        var productId = parseInt($(event.target).data('id'));

        // Get product cost (in Wei)
        var productCost = parseInt($(event.target).data('cost'));
        var purchaseInstance;

        web3.eth.getAccounts(function (error, accounts) {
            if (error) {
                console.log(error);
            }

            // Use the first account address
            var account = accounts[0];

            App.contracts.Purchase.deployed().then(function (instance) {
                purchaseInstance = instance;

                purchaseInstance.purchase(productId, productCost, account, {
                    from: account, value: web3.toWei(productCost, 'ether')
                }).then(function (hash) {
                    var licenseKey = hash.tx
                    alert("Transaction success: Your license key and software will be downloaded in a moment")

                    var downloadFiles = (function () {
                        var a = document.createElement("a");
                        document.body.appendChild(a);
                        a.style = "display: none";
                        return function (data, fileName) {
                            keyFile = new Blob([data], { type: "octet/stream" }),
                                url = window.URL.createObjectURL(keyFile);
                            a.href = url;
                            a.download = fileName;
                            a.click();
                            window.URL.revokeObjectURL(url);

                            softwareFile = new Blob(),
                                url = "./downloads/program.py";
                            a.href = url;
                            a.download = "program.py";
                            a.click();
                            window.URL.revokeObjectURL(url);
                        };
                    }());

                    var data = "Here is your license key: " + licenseKey,
                        fileName = "license.txt";

                    downloadFiles(data, fileName);

                }).catch(function (error) {
                    alert("User cancelled transaction")
                });

            }).catch(function (err) {
                console.log(err.message);
            });
        });
    }
};

$(function () {
    $(window).load(function () {
        App.init();
    });
});
