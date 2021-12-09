from web3 import Web3
from web3.contract import ContractEvent
from web3.types import TxParams
from contract_data import abi, bytecode


class Contract:
    def __init__(self, web3: Web3, address=''):
        self.__web3 = web3
        if address:
            self.__contract = web3.eth.contract(address=address, abi=abi)
        else:
            self.__contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    def deploy(self):
        tx_hash = self.__contract.constructor().transact()
        receipt = self.__web3.eth.waitForTransactionReceipt(tx_hash)
        self.__contract = self.__web3.eth.contract(
            address=receipt.contractAddress, abi=abi)
        self.owner_address = self.__web3.eth.defaultAccount
        return receipt

    def apply(
        self, hash: str, sender: str, nonce: int, gas: int
    ) -> TxParams:
        return self.__contract.functions.apply(
            hash).buildTransaction(
                {
                'from':sender,
                'nonce': nonce,
                'gas':gas
                }
            )


    def getApplicationID(self, email: str):
        return self.__contract.functions.getApplicationID(email).call()

    def wait(self, tx_hash):
        return self.__web3.eth.waitForTransactionReceipt(tx_hash)
