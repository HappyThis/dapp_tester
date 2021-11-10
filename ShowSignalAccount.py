from web3 import Web3

from main import conn_remote


def ShowSignalAccount(addr):
    print("addr:", addr, " balance:", conn_remote.eth.get_balance(Web3.toChecksumAddress(addr)))
