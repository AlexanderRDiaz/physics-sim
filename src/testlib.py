import os
import shutil
import sys


BIN_PATH = 'src/eyecandy/bin'
FRAMES_PATH = f'{BIN_PATH}/frames'


def GIFCleanup(self):
    if os.path.exists(FRAMES_PATH):
        shutil.rmtree(FRAMES_PATH)


def GIFSetup(self):
    if os.path.exists(FRAMES_PATH):
        shutil.rmtree(FRAMES_PATH)

    os.makedirs(FRAMES_PATH)


def GIFName(name: str) -> str:
    return os.path.basename(name)[5:-3]


def SoloRunOutput(name: str) -> None:
    path = 'src' + name.split('src')[1]

    print(f'Running {path}\nPython version: {sys.version}')
