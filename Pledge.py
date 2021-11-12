from conn import conn_remote, contract, private_key


def TakeMoneyToContract(value, pk=private_key):
    try:
        nonce = conn_remote.eth.getTransactionCount(conn_remote.eth.defaultAccount)
        gas = contract.functions.TakeMoneyToContract().estimateGas({"value": value})
        cur = contract.functions.TakeMoneyToContract().call({"value": value})
        tx = contract.functions.TakeMoneyToContract().buildTransaction({
            'chainId': conn_remote.eth.chainId,
            'gas': gas * 2,
            'gasPrice': conn_remote.eth.gasPrice * 2,
            'nonce': nonce,
            'value': value - gas * conn_remote.eth.gasPrice * 5
        })
        # 交易签名
        signed_tx = conn_remote.eth.account.sign_transaction(tx, pk)
        # 发往区块链
        conn_remote.eth.sendRawTransaction(signed_tx.rawTransaction)
        # 等待交易返回
        conn_remote.eth.waitForTransactionReceipt(signed_tx.hash)
        # 打印交易哈希
        tx_hash = conn_remote.toHex(conn_remote.keccak(signed_tx.rawTransaction))
        return_value = {
            'tx_hash': tx_hash,
            'cur': cur,
            'error': None,
        }
        print(return_value)
        return return_value
    except Exception as e:
        print(e)
        return_value = {
            'tx_hash': None,
            'error': e.__str__()
        }
        return return_value
