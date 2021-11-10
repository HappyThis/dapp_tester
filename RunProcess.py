import os
from multiprocessing.dummy import Process
from time import sleep


def runProcessForTest(num, dappdir="/home/ycq/DAPP/", keysdir="/home/ycq/keys/committees/", offset=0):
    for i in range(1 + offset, num + 1 + offset):
        os.chdir(dappdir)
        p = Process(target=testTask, kwargs={"id": i, "dir": dappdir, "keysdir": keysdir})
        p.start()
        sleep(0.5)
        os.chdir(os.getcwd())


def testTask(id, dir, keysdir):
    venv_python = dir + "venv/bin/python"
    print(venv_python + " " + "app.py -h 0.0.0.0 -p " + str(5000 + id) + " -c " + " " + keysdir + str(
        id) + "/config")
    os.system(
        venv_python + " " + "app.py -h 0.0.0.0 -p " + str(5000 + id) + " -c " + " " + keysdir + str(
            id) + "/config")
