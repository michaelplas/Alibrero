import os
from glob import glob
from shutil import rmtree


def deleteUpdater():
    path = os.getcwd()
    pattern = os.path.join(path, "Updater*")

    for item in glob(pattern):
        if not os.path.isdir(item):
            continue
        rmtree(item)


