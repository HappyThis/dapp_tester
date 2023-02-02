import os
import platform
from multiprocessing.dummy import Process
from time import sleep

from system_config.tester_config import dapp_main_file, dapp_listen, dapp_port


def runProcessForTest(num, dappdir, keysdir, offset=0):
    for i in range(1 + offset, num + 1 + offset):
        os.chdir(dappdir)
        p = Process(target=testTask, kwargs={"id": i, "dir": dappdir, "keysdir": keysdir})
        p.start()
        sleep(0.5)
        os.chdir(os.getcwd())


def testTask(id, dir, keysdir):
    if platform.system() == "Windows":
        venv_python = dir + "\\venv\\Scripts\\python.exe"
        config_file = "\\config"
        spt = "\\"
    elif platform.system() == "Linux":
        venv_python = dir + "venv/bin/python"
        config_file = "/config"
        spt = "/"
    else:
        print("unknown operating system")
        exit()
    print(venv_python + " " + dapp_main_file + " -h " + dapp_listen + " -p " + str(
        dapp_port + id) + " -c " + " " + keysdir + spt + str(
        id) + config_file)
    os.system(
        venv_python + " " + dapp_main_file + " -h " + dapp_listen + " -p " + str(
            dapp_port + id) + " -c " + " " + keysdir + spt + str(
            id) + config_file)
