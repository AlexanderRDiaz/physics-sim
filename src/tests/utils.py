import os
import shutil


BIN_PATH = 'src/tests/bin'
FRAMES_PATH = f'{BIN_PATH}/frames'


def cleanup(self):
    if os.path.exists(FRAMES_PATH):
        shutil.rmtree(FRAMES_PATH)


def setup(self):
    if os.path.exists(FRAMES_PATH):
        shutil.rmtree(FRAMES_PATH)

    os.makedirs(FRAMES_PATH)
