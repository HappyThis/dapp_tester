import os

from conn import keystroe


def Renumber():
    names = os.listdir(keystroe)
    num = 1
    for name in names:
        filePath = keystroe + '/' + name
        newPath = keystroe + '/' + str(num)
        os.rename(filePath, newPath)
        num += 1
