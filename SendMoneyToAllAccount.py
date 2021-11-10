import os

from SendMoneyToAccount import TakeMoneyToAddr
from main import keystroe


def ToValue(val):
    num = 0
    names = os.listdir(keystroe)
    for name in names:
        TakeMoneyToAddr(val, name)
        print(num)
        num += 1
