from web3 import Web3

from abi import abi
from system_config.tester_config import geth, rich_node

conn_local = Web3(Web3.IPCProvider("/home/ycq/geth/geth.ipc"))
conn_remote = Web3(Web3.HTTPProvider(geth))
conn_remote.eth.defaultAccount = Web3.toChecksumAddress(rich_node)
keystroe = "/home/ycq/keys/committees/"
contract_addr = '0x07AfA358C002Ef3B4597e64731b5cA15E4cf701f'
contract = conn_remote.eth.contract(address=conn_remote.toChecksumAddress(contract_addr), abi=abi)
current_noce = conn_remote.eth.getTransactionCount(conn_remote.eth.defaultAccount)

# 准备私钥
with open("password.pwd") as keyfile:
    encrypted_key = keyfile.read()
    private_key = conn_remote.eth.account.decrypt(encrypted_key, "123456")
