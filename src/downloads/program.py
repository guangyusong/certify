from solcx import set_solc_version, compile_files
from web3 import Web3

set_solc_version('v0.5.0')

# Contract Addresses. This needs to be manually configured.
activate_address = "0x77Ba6ECB94c9203Ef1E36b76733683764065B353"
purchase_address = "0xe7bF216b67aFb261C8D41fCBDd4153045234e0F8"


# Find Ganache Instance
# In the real world. This would be the address for the test network
GANACHE = "http://127.0.0.1:7545"

# Initialize web3 instance
w3 = Web3(Web3.HTTPProvider(GANACHE))

# Get our main account that we will be using
main_account = w3.eth.accounts[0]
w3.eth.defaultAccount = main_account

# In the real world we will be interacting with the blockchain directly
# and will not need this
""" Contract: Activate.sol """
# Directory to our contracts
compiled_sol = compile_files(
    ["./certify/contracts/Activate.sol"])

# dictionary with compiled code for a single contract
compiled_sol_keys = list(compiled_sol.keys())

contract_interface = compiled_sol.get(compiled_sol_keys[0])

# instantiate the contract, with specific contract address
activate_contract = w3.eth.contract(
    address=activate_address,
    abi=contract_interface['abi'],
    bytecode=contract_interface['bin'])

""" Contract: Purchase.sol"""
# Directory to our contracts.
compiled_sol2 = compile_files(
    ["./certify/contracts/Purchase.sol"])

# dictionary with compiled code for a single contract
compiled_sol_keys2 = list(compiled_sol2.keys())

contract_interface2 = compiled_sol2.get(compiled_sol_keys2[0])

# instantiate the contract, with specific contract address
purchase_contract = w3.eth.contract(
    address=purchase_address,
    abi=contract_interface2['abi'],
    bytecode=contract_interface2['bin'])


# Helper Functions from Sections
def exec_call(w3, contract_inst, function_name, *f_args):
    func_inst = contract_inst.get_function_by_name(function_name)
    return_value = func_inst(*f_args).call()
    return return_value


def exec_transact_receipt(w3, contract_inst, function_name, *f_args):
    func_inst = contract_inst.get_function_by_name(function_name)
    return_value = exec_call(w3, contract_inst, function_name, *f_args)
    tx_hash = func_inst(*f_args).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return return_value, tx_receipt


def exec_transact(w3, contract_inst, function_name, *f_args):
    rv, _ = exec_transact_receipt(w3, contract_inst, function_name, *f_args)
    return rv


# Check license
def check_license():
    # Part 1: Verify that the transaction hash exist
    while True:
        try:
            transaction_hash = input("Please enter your license key: ")
            print("Thank you. Checking for license key validity...")
            transaction = w3.eth.getTransaction(transaction_hash)
            print("Your license key is valid.")
            # Get the account that sent the transaction
            account = (transaction["from"])
            break
        except:
            print("Your license key is invalid. Please try again")

    # Part 2: Verify that the block exist
    while True:
        try:
            account in w3.eth.accounts
            print("Thank you. Comparing account info with our database...")
            break
        except:
            print(
                "Your account info does not match our database. Software will not activate.")

    # Load
    # Get transaction receipts from the hash / our license
    receipt = w3.eth.getTransactionReceipt(transaction_hash)
    # Get Events from the transaction receipt on our main contract
    logs = purchase_contract.events.transactionEvent().processReceipt(receipt)
    # Get our sale ID from the event
    saleId = logs[0].args._id

    # Part 3: Verify that the license has not been activated
    checkActive = activate_contract.functions.isActive(saleId).call()
    if False == checkActive:
        choice = input(
            "The software has not been activated, would you like to activate it? (y/n): \n")
        if choice == 'y':
            try:
                exec_transact(w3, activate_contract,
                              'activateProduct', saleId, transaction_hash)
                print("Congratulations, the software is now activated.")
                input("Type anything to exit... \n")
            except:
                print("Activation ERROR")
        else:
            print(
                "User chose to terminate the activation process. Software not activated.")
            input("Type anything to exit... \n")
    elif True == checkActive:
        print("Key is invalid...Please purchase a new key.")
    else:
        print("An unknown error has occured. The program will now terminate.")


check_license()
