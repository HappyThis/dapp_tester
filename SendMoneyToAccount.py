from web3 import Web3

from conn import conn_remote


def TakeMoneyToAddr(value, addr):
    try:
        conn_remote.eth.sendTransaction(
            {
                "from": Web3.toChecksumAddress("419b94500d78a8e48f30bfc569311b2ce992b1fa"),
                "to": Web3.toChecksumAddress(addr),
                "value": value,
            }
        )
    except Exception as e:
        print(e)
