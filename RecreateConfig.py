import configparser
import os
import shutil

from conn import keystroe


def genConfig():
    names = os.listdir(keystroe)
    for name in names:
        cf = configparser.ConfigParser()
        cf.read("init_config")
        cf.set("SYSTEM", "bc_pwd_file", "/home/ycq/keys/committees/" + name + "/pwd")
        cf.set("SYSTEM", "log", name)
        cf.write(open("system_config/init_config", "w"))
        shutil.copy("system_config/init_config", keystroe + name)
