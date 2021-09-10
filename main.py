import json
import os
import getopt
import sys

from web3 import Web3
from abi import abi

conn_local = Web3(Web3.IPCProvider("/home/ycq/geth/geth.ipc"))
conn_remote = Web3(Web3.HTTPProvider("http://10.112.147.205:8545"))
conn_remote.eth.defaultAccount = Web3.toChecksumAddress('419b94500d78a8e48f30bfc569311b2ce992b1fa')
keystroe = "/home/ycq/geth/keystore"
contract_addr = '0x07AfA358C002Ef3B4597e64731b5cA15E4cf701f'
contract = conn_remote.eth.contract(address=conn_remote.toChecksumAddress(contract_addr), abi=abi)

current_noce = conn_remote.eth.getTransactionCount(conn_remote.eth.defaultAccount)

# 准备私钥
with open("password.pwd") as keyfile:
    encrypted_key = keyfile.read()
    private_key = conn_remote.eth.account.decrypt(encrypted_key, "123456")


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


def TakeMoneyToAddr(value, addr):
    # global current_noce
    # addr = Web3.toChecksumAddress(addr)
    # try:
    #     gas = contract.functions.TakeMoneyToAddr(addr, value).estimateGas()
    #     cur = contract.functions.TakeMoneyToAddr(addr, value).call()
    #     tx = contract.functions.TakeMoneyToAddr(addr, value).buildTransaction({
    #         'chainId': conn_remote.eth.chainId,
    #         'gas': gas * 2,
    #         'gasPrice': conn_remote.eth.gasPrice * 2,
    #         'nonce': current_noce,
    #     })
    #     current_noce += 1
    #     # 交易签名
    #     signed_tx = conn_remote.eth.account.sign_transaction(tx, private_key)
    #     # 发往区块链
    #     conn_remote.eth.sendRawTransaction(signed_tx.rawTransaction)
    #     # # 等待交易返回
    #     # conn_remote.eth.waitForTransactionReceipt(signed_tx.hash)
    #     # # 打印交易哈希
    #     tx_hash = conn_remote.toHex(conn_remote.keccak(signed_tx.rawTransaction))
    #     return_value = {
    #         'tx_hash': tx_hash,
    #         'cur': cur,
    #         'error': None
    #     }
    #     # print(return_value)
    #     return return_value
    # except Exception as e:
    #     current_noce -= 1
    #     print(e)
    #     return_value = {
    #         'tx_hash': None,
    #         'error': e.__str__()
    #     }
    #     return return_value
    conn_remote.eth.sendTransaction(
        {
            "from": Web3.toChecksumAddress("419b94500d78a8e48f30bfc569311b2ce992b1fa"),
            "to": Web3.toChecksumAddress(addr),
            "value": value,
        }
    )


def Gen_New_Accounts(num, val=0):
    for i in range(0, num):
        conn_local.geth.personal.newAccount("123456")
    names = os.listdir(keystroe)
    for name in names:
        old_path = keystroe + '/' + name
        name_len = len(name)
        if name_len <= 40:
            continue
        new_name = name[name_len - 40:]
        if val > 0:
            TakeMoneyToAddr(val, new_name)
        new_path = keystroe + '/' + new_name
        print(new_path)
        os.rename(old_path, new_path)


def ShowAllAccounts():
    num = 1
    names = os.listdir(keystroe)
    for name in names:
        print("(", num, ")", "addr:", name, " balance:", conn_remote.eth.get_balance(Web3.toChecksumAddress(name)))
        num += 1


def ShowSignalAccount(addr):
    print("addr:", addr, " balance:", conn_remote.eth.get_balance(Web3.toChecksumAddress(addr)))


def ToValue(val):
    num = 0
    names = os.listdir(keystroe)
    for name in names:
        TakeMoneyToAddr(val, name)
        print(num)
        num += 1


def Average():
    avg_val = int(1e18)
    num = 1
    names = os.listdir(keystroe)
    names.sort()
    for name in names:
        if len(name) > 40:
            print("(", num, ")", "addr:", name)
            continue
        bal = conn_remote.eth.get_balance(Web3.toChecksumAddress(name))
        filePath = keystroe + '/' + name
        # 准备私钥
        with open(filePath) as keyfile:
            ek = keyfile.read()
            pk = conn_remote.eth.account.decrypt(ek, "123456")
        if bal >= avg_val:
            os.rename(filePath, filePath + "*")
            print("add *")
            continue
            # sub = bal - avg_val
            # conn_remote.eth.defaultAccount = Web3.toChecksumAddress(name)
            # TakeMoneyToContract(sub, pk)
            # conn_remote.eth.defaultAccount = Web3.toChecksumAddress('0x801FD03AfBe1c9FCBaE77bDc03C7812Ad9776d60')
        if bal < avg_val:
            sub = avg_val - bal
            return_value = TakeMoneyToAddr(sub, name)
            if return_value["tx_hash"] is None:
                break
            os.rename(filePath, filePath + "*")
        # bal_next = conn_remote.eth.get_balance(Web3.toChecksumAddress(name))
        print("(", num, ")", "addr:", name)
        num += 1


def number():
    names = os.listdir(keystroe)
    for name in names:
        filePath = keystroe + '/' + name
        file = open(filePath)
        jsonFile = json.load(file)
        addrFromPwd = jsonFile['address']
        newPath = keystroe + '/' + addrFromPwd
        os.rename(filePath, newPath)


def usage():
    print(
        "[--gen or -g] value [wei]:生成value个账户，每个账户初始化wei个金币\n"
        "[--list or -l] addr or all:查看所有账户以及金额或者特定账户的金额\n"
        "[--tx or -t] addr wei:给addr打wei个金币\n"
        '[--money or -m] num 向智能合约发送num个金币'
        '[--num or n]'
    )


if len(sys.argv) == 1:
    usage()
    sys.exit()
try:
    opts, args = getopt.getopt(sys.argv[1:], "hl:g:t:m:ans",
                               ["help", "list=", "gen=", "tx=", "money=", "avg", "num", "send"])
except getopt.GetoptError:
    print("argv error,please input")

for opt, arg in opts:
    if opt == '-h' or opt == '--help':
        usage()
    elif opt == '-l' or opt == '--list':
        arg = str.strip(arg)
        spilt_arg = str.split(arg, " ")
        if "all" in spilt_arg:
            ShowAllAccounts()
        elif len(spilt_arg[0]) == 40:
            ShowSignalAccount(spilt_arg[0])
        else:
            print("arg error")
    elif opt == '-g' or opt == '--gen':
        arg = str.strip(arg)
        spilt_arg = str.split(arg, ",")
        if len(spilt_arg) == 1:
            Gen_New_Accounts(int(spilt_arg[0]))
        elif len(spilt_arg) == 2:
            num = int(spilt_arg[1])
            current_noce = conn_remote.eth.getTransactionCount(conn_remote.eth.defaultAccount)
            Gen_New_Accounts(int(spilt_arg[0]), num)
            continue
        else:
            print("arg error")
    elif opt == '-t' or opt == '--tx':
        arg = str.strip(arg)
        spilt_arg = str.split(arg, ",")
        to = spilt_arg[0]
        num = int(spilt_arg[1])
        current_noce = conn_remote.eth.getTransactionCount(conn_remote.eth.defaultAccount)
        TakeMoneyToAddr(num, to)
    elif opt == '-m' or opt == '--money':
        arg = str.strip(arg)
        num = int(arg)
        TakeMoneyToContract(num)
    elif opt == '-a' or opt == '--avg':
        Average()
    elif opt == '-n' or opt == '--num':
        number()
    elif opt == '-s' or opt == '--send':
        ToValue(int(1e18))
