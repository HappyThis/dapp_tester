import configparser
import os
import shutil

from main import keystroe


def genConfig():
    names = os.listdir(keystroe)
    for name in names:
        cf = configparser.ConfigParser()
        cf.read("config")
        cf.set("SYSTEM", "bc_pwd_file", "/home/ycq/keys/committees/" + name + "/pwd")
        cf.set("SYSTEM", "log", name)
        cf.write(open("config", "w"))
        shutil.copy("config", keystroe + name)
