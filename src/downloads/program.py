from solcx import set_solc_version, compile_files
from web3 import Web3

set_solc_version('v0.5.0')

# Find Ganache Instance
# In the real world. This would be the address for the test network
GANACHE = "http://127.0.0.1:7545"

# Initialize web3 instance
w3 = Web3(Web3.HTTPProvider(GANACHE))

# Get our main account that we will be using
main_account = w3.eth.accounts[0]
w3.eth.defaultAccount = main_account

# In the real world we won't need this
compiled_sol = compile_files(
    ["./contracts/Purchase.sol"])  # Compiled source code

# dictionary with compiled code for a single contract
compiled_sol_keys = list(compiled_sol.keys())

contract_interface = compiled_sol.get(compiled_sol_keys[0])

contract_address = "0xf442BdB194b91625C2628532834a445f41Cd9AA9"

# instantiate the contract, with specific contract address
purchase_contract = w3.eth.contract(
    address=contract_address,
    abi=contract_interface['abi'],
    bytecode=contract_interface['bin'])

# execute a call, which does not execute a transaction (i.e. no write => no gas)


def exec_call(w3, contract_inst, function_name, *f_args):
    func_inst = contract_inst.get_function_by_name(function_name)

    return_value = func_inst(*f_args).call()
    return return_value

# execute a transaction (i.e. a write), and return the transaction receipt (costs gas paid in Ether)


def exec_transact_receipt(w3, contract_inst, function_name, *f_args):
    func_inst = contract_inst.get_function_by_name(function_name)

    # get the return value, without executing transaction
    return_value = exec_call(w3, contract_inst, function_name, *f_args)

    # execute the transaction
    tx_hash = func_inst(*f_args).transact()
    # receipt does not contain values returned by function
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return return_value, tx_receipt

# execute transaction, but ignore the receipt


def exec_transact(w3, contract_inst, function_name, *f_args):
    rv, _ = exec_transact_receipt(w3, contract_inst, function_name, *f_args)
    return rv


def check_license():
    # Part 1: Verify that the transaction hash exist
    while True:
        try:
            transaction_hash = input("Please enter your license key: ")
            print("Thank you. Checking...")
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
            print("Thank you. Checking...")
            break
        except:
            print(
                "Your account info does not match our database. Software will not activate.")

    # Get transaction receipts from the hash / our license
    receipt = w3.eth.getTransactionReceipt(transaction_hash)
    # Get Events from the transaction receipt
    logs = purchase_contract.events.transactionEvent().processReceipt(receipt)
    # Get our sale ID
    saleId = logs[0].args._id

    # Part 3: Verify that the license has not been activated
    checkActive = purchase_contract.functions.isActive(saleId).call()
    if False == checkActive:
        choice = input(
            "The software has not been activated, would you like to activate it? (y/n)")
        if choice == 'y':
            try:
                exec_transact(w3, purchase_contract,
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
        print("Software is already activated!!")
    else:
        print("An unknown error has occured. The program will now terminate.")


check_license()
