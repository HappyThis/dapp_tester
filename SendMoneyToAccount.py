from web3 import Web3

from conn import conn_remote


def TakeMoneyToAddr(value, addr):
    try:
        conn_remote.eth.sendTransaction(
            {
                "from": Web3.toChecksumAddress("a49c39f2271b9d105d2ab444d2bee72820d0caf0"),
                "to": Web3.toChecksumAddress(addr),
                "value": value,
            }
        )
    except Exception as e:
        print(e)
