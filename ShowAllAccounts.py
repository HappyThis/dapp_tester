import json
import os

from web3 import Web3

from main import keystroe


def ShowAllAccounts():
    num = 1
    names = os.listdir(keystroe)
    names.sort()
    for name in names:
        filePath = keystroe + '/' + name
        file = open(filePath)
        jsonFile = json.load(file)
        addr = jsonFile['address']
        # print("(", num, ")", "addr:", addr, " balance:", conn_remote.eth.get_balance(Web3.toChecksumAddress(addr)))
        print("\"" + Web3.toChecksumAddress(addr) + "\",")
        num += 1
