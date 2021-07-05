import os
import getopt
import sys

from web3 import Web3
from web3.middleware import geth_poa_middleware

conn_local = Web3(Web3.IPCProvider("/home/ycq/geth/geth.ipc"))
conn_remote = Web3(Web3.WebsocketProvider("wss://rinkeby.infura.io/ws/v3/7ecf51085fe840f49fcea75636976335"))
conn_remote.eth.defaultAccount = Web3.toChecksumAddress('0x801FD03AfBe1c9FCBaE77bDc03C7812Ad9776d60')
keystroe = "/home/ycq/geth/keystore"


def Gen_New_Accounts(num):
    for i in range(0, num):
        conn_local.geth.personal.newAccount("123456")
    names = os.listdir(keystroe)
    for name in names:
        old_path = keystroe + '/' + name
        print(old_path)
        name_len = len(name)
        if name_len <= 40:
            continue
        new_name = name[name_len - 40:]
        new_path = keystroe + '/' + new_name
        print(new_path)
        os.rename(old_path, new_path)


def ShowAllAccounts():
    names = os.listdir(keystroe)
    for name in names:
        print("addr:", name, " balance:", conn_remote.eth.get_balance(Web3.toChecksumAddress(name)))


def ShowSignalAccount(addr):
    print("addr:", addr, " balance:", conn_remote.eth.get_balance(Web3.toChecksumAddress(addr)))


def GiveWei(addr, num):
    try:
        tx = conn_remote.eth.sendTransaction({
            "from": conn_remote.eth.defaultAccount,
            "to": Web3.toChecksumAddress(addr),
            "value": num,
            "gas": 30000,
        })
        signed_tx = conn_remote.eth.account.sign_transaction(tx, private_key)
        conn_remote.eth.sendRawTransaction(signed_tx.rawTransaction)
        conn_remote.eth.waitForTransactionReceipt(signed_tx.hash)
        tx_hash = conn_remote.toHex(conn_remote.keccak(signed_tx.rawTransaction))
        # print(tx_hash)
    except Exception as e:
        print(e)


def usage():
    print(
        "[--gen or -g] value [wei]:生成value个账户，每个账户初始化wei个金币\n"
        "[--list or -l] addr or all:查看所有账户以及金额或者特定账户的金额\n"
        "[--tx or -t] addr wei:给addr打wei个金币"
    )


if len(sys.argv) == 1:
    usage()
    sys.exit()
try:
    opts, args = getopt.getopt(sys.argv[1:], "hl:g:t:",
                               ["help", "list=", "gen=", "tx="])
except getopt.GetoptError:
    print("argv error,please input")

# 准备私钥
with open("password.pwd") as keyfile:
    encrypted_key = keyfile.read()
    private_key = conn_remote.eth.account.decrypt(encrypted_key, "ycq5512494")
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
        spilt_arg = str.split(arg, " ")
        if len(spilt_arg) == 1:
            Gen_New_Accounts(int(spilt_arg[0]))
        elif len(spilt_arg) == 2:
            continue
        else:
            print("arg error")

    elif opt == '-t' or opt == '--tx':
        arg = str.strip(arg)
        spilt_arg = str.split(arg, " ")
        to = spilt_arg[0]
        num = int(spilt_arg[1])
        GiveWei(to, num)
