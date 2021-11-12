import os
from conn import keystroe, conn_local


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
            from SendMoneyToAccount import TakeMoneyToAddr
            TakeMoneyToAddr(val, new_name)
        new_path = keystroe + '/' + new_name
        print(new_path)
        os.rename(old_path, new_path)
