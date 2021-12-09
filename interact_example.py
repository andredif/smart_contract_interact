import json

from web3 import Web3, HTTPProvider
from eth_account import Account

from .contracts.contract import Contract

acct = Account.create('KEYSMASH FJAFJKLDSKF7JKFDJ 1530')

WEB3_INFURA_URL = "https://ropsten.infura.io/v3/809192a86ed049d6ad649be711b436e8"
contract_address = "0xcbbfbafedb0eb83016d2a96a4e80d30b20fa3e30"
with open('./contract.abi') as abi_file:
    abi = json.load(abi_file)
email = b"difranco.developer@gmail.com"

if __name__=="__main__":
    # create web3 instance
    w3 = Web3(HTTPProvider(WEB3_INFURA_URL))
    if not w3.isConnected():
        raise 'Connection to ethereum node failed'
    email_hash = Web3.solidityKeccak(['bytes32'],[email])
    # get Ethereum address and private key from Account
    address = Web3.toChecksumAddress(contract_address)
    manager_password = acct.key
    manager_address = Web3.toChecksumAddress(acct.address)
    #request test Ether from faucet
    input(f"wait for {manager_address} to be fauceted")
    w3.eth.default_account = manager_address
    #create new Contract Instance
    contract = Contract(w3, address)
    curr_nonce = w3.eth.get_transaction_count(manager_address)
    #build transaction
    build_tx = contract.apply(
        email_hash, manager_address, gas=10000
    )
    # sign transaction
    sign_tx = w3.eth.account.sign_transaction(build_tx, manager_password) 
    # send the transaction
    tx_hash = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
    this_id = contract.contract.functions.getApplicationID('difranco.developer@gmail.com').call()