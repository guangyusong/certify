from solcx import set_solc_version, compile_files
from web3 import Web3

# Set Solc version
set_solc_version('v0.5.0')

# Find Ganache Instance
GANACHE = "http://127.0.0.1:7545"

# Initialize web3 instance
w3 = Web3(Web3.HTTPProvider(GANACHE))


def get_account():

    # Use the account
    user_account = w3.eth.accounts[0]

    # set default account on web3 object
    w3.eth.defaultAccount = user_account


def check_license():

    while True:
        try:
            transaction_hash = input("Please enter your license key: ")
            print("Thank you. Checking...")
            transaction = w3.eth.getTransaction(transaction_hash)
            # Get the account that sent the transaction
            account = (transaction["from"])
            break
        except:
            print("Your license key is invalid. Please try again")

    try:
        account in w3.eth.accounts
        print("Congratulations, the software is now activated.")
    except:
        print("Your account info does not match our database. Software will not activate.")


check_license()
