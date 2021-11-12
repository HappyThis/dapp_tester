import getopt
import sys

from GenNewAccounts import Gen_New_Accounts
from Pledge import TakeMoneyToContract
from RecreateConfig import genConfig
from RenumberToAllAccount import Renumber
from RunProcess import runProcessForTest
from SendMoneyToAccount import TakeMoneyToAddr
from SendMoneyToAllAccount import ToValue
from ShowAllAccounts import ShowAllAccounts
from ShowSignalAccount import ShowSignalAccount
from conn import conn_remote


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
    opts, args = getopt.getopt(sys.argv[1:], "hl:g:t:m:anscr:",
                               ["help", "list=", "gen=", "tx=", "money=", "avg", "num", "send", "cfg", "run="])
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
    elif opt == '-n' or opt == '--num':
        Renumber()
    elif opt == '-s' or opt == '--send':
        ToValue(int(1e18))
    elif opt == '-r' or opt == '--run':
        num = int(arg)
        runProcessForTest(num)
    elif opt == '-c' or opt == '--cfg':
        genConfig()
