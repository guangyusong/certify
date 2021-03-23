# Certify

#### This is a software licensing application built using Solidity to experiment with the Ethereum blockchain.  
![image](https://user-images.githubusercontent.com/15316444/112085478-fc3e6180-8b60-11eb-9571-03b16ce42d15.png)

#### Dependencies
- Ubuntu 18.04 (Should also work on 16.04 or 14.04)
- Python3
- Solidity 0.5.0
- Node.js (created with v8.10.0)
- Ganache
- Truffle
- Metamask Browser Extension

#### Installation and Runtime instructions on a local Ganache blockchain:
- Setup an Ubuntu VM (or machine if you have one). Obtain and install all listed dependencies from the internet.
- Ensure that the repository is cloned in your "Downloads" folder on Ubuntu.
- Start Ganache, ensure that the RPC server is set to: http://127.0.0.1:7545
- Check in Ganache and verify that your workspace is using truffle-config.js
- Go into the "Certify/" directory, open a terminal and type: ```npm install```
- After the dependencies are installed, in the terminal type: ```truffle compile && truffle migrate```
- Open "Certify/src/downloads/program.py". On the top, replace the variable "activate_address" with the address of the Activate contract in Ganache, then do the same with "purchase_address" and the address of the Purchase contract. Note that this is because we are testing on a local instance and the newly migrated contracts will have different addresses. If we have an instance deployed in the real world then everyone will be using the same address and there will be no need to replace the address.
- To start the Web GUI, open a terminal in the "Certify/" directory and type: ```npm run dev```
- Click on the buttons on the page to purchase products with Metamask
- On successful purchase, the license key and the software will be available for download. The user can then run the downloaded software with python and it will prompt you to enter the key and activate the software. Once the software is already activated, it cannot be activated again.

References:
- https://techmalak.com/hope-windows-9-better-windows-8/
- https://github.com/mdbootstrap/Ecommerce-Template-Bootstrap
- https://www.trufflesuite.com/tutorials/pet-shop
